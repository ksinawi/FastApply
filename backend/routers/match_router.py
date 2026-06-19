from fastapi import APIRouter

from services.matcher import match_resume_to_job

router = APIRouter()

@router.post("/match")
async def match(data: dict):
    resume = data[resume]
    job = data[job]

    result = match_resume_to_job(resume, job)

    return result
