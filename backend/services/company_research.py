from services.llm_client import client
from utils.prompts import COMPANY_RESEARCH_PROMPT

RESEARCH_MODEL = "gpt-4.1-mini"

def research_company(company: str, job_title: str) -> str:
    if not company or not company.strip():
        return ""

    prompt = COMPANY_RESEARCH_PROMPT.format(company=company, job_title=job_title or "")

    try:
        response = client.responses.create(
            model=RESEARCH_MODEL,
            input=prompt,
            tools=[{"type": "web_search_preview"}],
        )
    except Exception as error:
        print(f"[company_research] lookup failed for '{company}', skipping: {error}")
        return ""

    return (response.output_text or "").strip()
