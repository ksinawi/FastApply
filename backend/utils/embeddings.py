import math

from core.config import settings
from services.llm_client import get_client


async def get_embeddings(texts: list[str]) -> list[list[float]]:
    if not texts:
        return []

    response = await get_client().embeddings.create(model=settings.embedding_model, input=texts)

    ordered = sorted(response.data, key=lambda item: item.index)

    return [item.embedding for item in ordered]


def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot / (norm_a * norm_b)
