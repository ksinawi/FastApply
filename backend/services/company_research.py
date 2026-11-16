import logging

from core.config import settings
from services.llm_client import get_client
from utils.prompts import COMPANY_RESEARCH_PROMPT

logger = logging.getLogger(__name__)


async def research_company(company: str, job_title: str) -> str:
    """Best-effort web research on the company. Returns "" on any failure."""
    if not company or not company.strip():
        return ""

    prompt = COMPANY_RESEARCH_PROMPT.format(company=company, job_title=job_title or "")

    try:
        response = await get_client().responses.create(
            model=settings.research_model,
            input=prompt,
            tools=[{"type": "web_search_preview"}],
        )
    except Exception:
        logger.warning("Company research failed for %r, continuing without it", company, exc_info=True)
        return ""

    return (response.output_text or "").strip()
