from schemas.job import Job
from utils.llm import call_llm
from utils.prompts import JOB_ANALYZER_PROMPT


async def analyze_job(job_description: str) -> Job:
    return await call_llm(JOB_ANALYZER_PROMPT.format(job=job_description), Job)
