from fastapi import APIRouter, UploadFile, File, Form

from services.resume_parser import extract_text
from services.resume_analyzer import analyze_resume
from services.job_analyzer import analyze_job
from services.matcher import match_resume_to_job
from services.tailor import tailor_resume

router = APIRouter()

@router.post("/process_application")
async def process_application_endpoint(file: UploadFile = File(...), job_description: str = Form(...)):

    file_bytes = await file.read()
    file_text = extract_text(file_bytes)

    file_data = analyze_resume(file_text)
    job_data = analyze_job(job_description)

    match_data = match_resume_to_job(file_data, job_data)

    tailor_data = tailor_resume(file_data, job_data, match_data)

    return {
        "matchedSkills": match_data.get("matched_skills", []),
        "missingKeywords": match_data.get("missing_skills", []),
        "matchScore": match_data.get("match_score", 0),
        "recommendations": tailor_data.get("recommendations", []),
        "tailoredContent": tailor_data.get("tailored_resume", [])
    }
