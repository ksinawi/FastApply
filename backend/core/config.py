"""Application settings, read once from environment variables (and .env in development)."""
import os
from dataclasses import dataclass, field

from dotenv import load_dotenv

load_dotenv()


def _list(name: str, default: str) -> list[str]:
    return [item.strip().rstrip("/") for item in os.getenv(name, default).split(",") if item.strip()]


@dataclass(frozen=True)
class Settings:
    openai_api_key: str = field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))

    llm_model: str = field(default_factory=lambda: os.getenv("LLM_MODEL", "gpt-4.1-mini"))
    research_model: str = field(default_factory=lambda: os.getenv("RESEARCH_MODEL", "gpt-4.1-mini"))
    embedding_model: str = field(default_factory=lambda: os.getenv("EMBEDDING_MODEL", "text-embedding-3-small"))
    llm_timeout_seconds: float = field(default_factory=lambda: float(os.getenv("LLM_TIMEOUT_SECONDS", "90")))

    # Comma-separated list of exact origins, e.g. "https://fastapply.vercel.app,http://localhost:3000"
    allowed_origins: list[str] = field(default_factory=lambda: _list("ALLOWED_ORIGINS", "http://localhost:3000"))
    # Optional regex for extra origins, e.g. Vercel preview deployments: "https://fastapply-.*\.vercel\.app"
    allowed_origin_regex: str | None = field(default_factory=lambda: os.getenv("ALLOWED_ORIGIN_REGEX") or None)

    max_upload_bytes: int = field(default_factory=lambda: int(float(os.getenv("MAX_UPLOAD_MB", "5")) * 1024 * 1024))
    max_job_description_chars: int = field(default_factory=lambda: int(os.getenv("MAX_JOB_DESCRIPTION_CHARS", "20000")))
    max_document_chars: int = field(default_factory=lambda: int(os.getenv("MAX_DOCUMENT_CHARS", "30000")))

    # Analysis requests allowed per client IP per window. 0 disables rate limiting.
    rate_limit_requests: int = field(default_factory=lambda: int(os.getenv("RATE_LIMIT_REQUESTS", "10")))
    rate_limit_window_seconds: int = field(default_factory=lambda: int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "3600")))

    log_level: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO").upper())


settings = Settings()
