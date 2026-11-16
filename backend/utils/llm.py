import logging
from typing import Any, TypeVar

from fastapi import HTTPException
from openai import OpenAIError
from openai.lib._pydantic import to_strict_json_schema
from pydantic import BaseModel, ValidationError

from core.config import settings
from services.llm_client import get_client

logger = logging.getLogger(__name__)

ModelT = TypeVar("ModelT", bound=BaseModel)

def _clean_schema(node: Any) -> Any:
    """Drop the `default` and `title` annotations Pydantic adds; strict mode rejects them."""
    if isinstance(node, list):
        return [_clean_schema(item) for item in node]
    if not isinstance(node, dict):
        return node

    cleaned = {}
    for key, value in node.items():
        if key == "properties" and isinstance(value, dict):
            # Keys here are field names (a field may legitimately be called "title").
            cleaned[key] = {name: _clean_schema(sub) for name, sub in value.items()}
        elif key == "default" or (key == "title" and isinstance(value, str)):
            continue
        else:
            cleaned[key] = _clean_schema(value)
    return cleaned


def response_format(model: type[BaseModel]) -> dict:
    """A strict JSON-schema response format for the OpenAI Responses API."""
    return {
        "type": "json_schema",
        "name": model.__name__,
        "strict": True,
        "schema": _clean_schema(to_strict_json_schema(model)),
    }


async def call_llm(prompt: str, model: type[ModelT]) -> ModelT:
    """Call the LLM and return its answer parsed into `model`.

    Uses structured outputs, so the response is guaranteed to match the schema.
    """
    try:
        response = await get_client().responses.create(
            model=settings.llm_model,
            input=prompt,
            text={"format": response_format(model)},
        )
    except OpenAIError as error:
        logger.exception("LLM request failed")
        raise HTTPException(status_code=502, detail="The AI service is unavailable right now. Please try again in a moment.") from error

    if response.status != "completed":
        reason = getattr(response.incomplete_details, "reason", None) or response.status
        logger.warning("LLM response incomplete: %s", reason)
        raise HTTPException(status_code=502, detail="The AI response was cut off. Please try again.")

    output_text = (response.output_text or "").strip()

    if not output_text:
        raise HTTPException(status_code=502, detail="The AI returned an empty response. Please try again.")

    try:
        return model.model_validate_json(output_text)
    except ValidationError as error:
        logger.warning("LLM output failed validation: %s", error)
        raise HTTPException(status_code=502, detail="The AI returned an unexpected response. Please try again.") from error
