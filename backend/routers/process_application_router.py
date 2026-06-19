from fastapi import APIRouter
from pydantic import BaseModel

from services.resume_analyzer import analyze_resume
from services.job_analyzer import analyze_job
from services.matcher import match_resume_to_job
from services.tailor import tailor_resume

router = APIRouter()

class Application(BaseModel):
    resume: dict
    job: dict


@router.post("/process_application")
def process_application_endpoint(data: Application):
    
    resume_input = data.resume
    job_input = data.job

    resume_data = analyze_resume(resume_input)
    job_data = analyze_job(job_input)

    match_data = match_resume_to_job(resume_data, job_data)

    tailor_data = tailor_resume(resume_data, job_data, match_data)

    return {
        "resume": resume_data,
        "job": job_data,
        "match": match_data,
        "tailor": tailor_data
    }
