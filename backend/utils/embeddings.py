import math

from fastapi import HTTPException
from openai import OpenAIError

from services.llm_client import client

EMBEDDING_MODEL = "text-embedding-3-small"

def get_embeddings(texts: list[str]) -> list[list[float]]:
    if not texts:
        return []

    try:
        response = client.embeddings.create(model=EMBEDDING_MODEL, input=texts)
    except OpenAIError as error:
        raise HTTPException(status_code=502, detail=f"The AI provider request failed: {error}")

    ordered = sorted(response.data, key=lambda item: item.index)

    return [item.embedding for item in ordered]

def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot / (norm_a * norm_b)
