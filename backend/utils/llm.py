import json

from fastapi import HTTPException
from openai import OpenAIError

from services.llm_client import client

def _strip_markdown_fence(text: str) -> str:
    text = text.strip()

    if not text.startswith("```"):
        return text

    text = text.strip("`").strip()

    if text.lower().startswith("json"):
        text = text[4:].strip()

    return text

def call_llm(prompt: str):
    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt,
        )
    except OpenAIError as error:
        raise HTTPException(status_code=502, detail=f"The AI provider request failed: {error}")

    if response.status != "completed":
        reason = getattr(response.incomplete_details, "reason", None) or response.status
        raise HTTPException(status_code=502, detail=f"The AI response did not complete ({reason}). Please try again.")

    output_text = _strip_markdown_fence(response.output_text or "")

    if not output_text:
        raise HTTPException(status_code=502, detail="The AI returned an empty response. Please try again.")

    try:
        return json.loads(output_text)
    except json.JSONDecodeError:
        raise HTTPException(status_code=502, detail="The AI returned a response that could not be parsed. Please try again.")
