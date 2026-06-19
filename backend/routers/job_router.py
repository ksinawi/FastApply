from fastapi import APIRouter

from services.job_analyzer import analyze_job

router = APIRouter()

@router.post("/analyze_job")
async def analyze_job(data: dict):
    job_description = data[job_description]
    return analyze_job(job_description)