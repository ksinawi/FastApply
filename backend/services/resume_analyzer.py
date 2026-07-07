from services.llm_client import client
from schemas.resume import Resume
from utils.prompts import RESUME_ANALYZER_PROMPT
from utils.llm import call_llm

def analyze_resume(resume_text) -> Resume:
    prompt = RESUME_ANALYZER_PROMPT.format(resume=resume_text)

    data = call_llm(prompt)

    return Resume.model_validate(data)