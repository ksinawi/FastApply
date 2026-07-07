from services.llm_client import client
from schemas.tailored import TailoredResume
from utils.prompts import TAILOR_PROMPT
from utils.llm import call_llm

def tailor_resume(resume, job, match) -> TailoredResume:
    prompt = TAILOR_PROMPT.format(
        resume=resume.model_dump_json(indent=2),
        job=job.model_dump_json(indent=2),
        match=match.model_dump_json(indent=2),
    )

    data = call_llm(prompt)

    return TailoredResume.model_validate(data)