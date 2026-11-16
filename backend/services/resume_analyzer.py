from schemas.resume import Resume
from utils.llm import call_llm
from utils.prompts import RESUME_ANALYZER_PROMPT


async def analyze_resume(resume_text: str) -> Resume:
    return await call_llm(RESUME_ANALYZER_PROMPT.format(resume=resume_text), Resume)
