from functools import lru_cache

from openai import AsyncOpenAI

from core.config import settings


@lru_cache(maxsize=1)
def get_client() -> AsyncOpenAI:
    return AsyncOpenAI(api_key=settings.openai_api_key, timeout=settings.llm_timeout_seconds, max_retries=2)
