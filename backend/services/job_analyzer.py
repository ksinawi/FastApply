from services.llm_client import client
from schemas.job import Job
from utils.prompts import JOB_ANALYZER_PROMPT
from utils.llm import call_llm


def analyze_job(job_description) -> Job:
    prompt = JOB_ANALYZER_PROMPT.format(job=job_description)

    data = call_llm(prompt)

    return Job.model_validate(data)
