from fastapi import APIRouter, UploadFile, File, Form

from services.resume_parser import extract_text
from services.resume_analyzer import analyze_resume
from services.job_analyzer import analyze_job
from services.matcher import match_resume_to_job
from services.tailor import tailor_resume

router = APIRouter()

@router.post("/process_application")
async def process_application_endpoint(resume_file: UploadFile = File(...), job: str = Form(...)):

    resume_bytes = await resume_file.read()
    resume_text = extract_text(resume_bytes)

    resume_data = analyze_resume(resume_text)
    job_data = analyze_job(job)

    match_data = match_resume_to_job(resume_data, job_data)

    tailor_data = tailor_resume(resume_data, job_data, match_data)

    return {
        "resume": resume_data,
        "job": job_data,
        "match": match_data,
        "tailor": tailor_data
    }
