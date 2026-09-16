from fastapi import APIRouter, HTTPException, UploadFile, File, Form

from services.document_parser import extract_text
from services.resume_analyzer import analyze_resume
from services.job_analyzer import analyze_job
from services.matcher import match_resume_to_job
from services.tailor import tailor_resume

from schemas.responses import ProcessApplicationResponse

router = APIRouter()

@router.post("/process_application", response_model=ProcessApplicationResponse)
async def process_application_endpoint(file: UploadFile = File(...), job_description: str = Form(...)):

    file_bytes = await file.read()

    try:
        file_text = extract_text(file.filename, file_bytes)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    file_data = analyze_resume(file_text)
    job_data = analyze_job(job_description)

    match_data = match_resume_to_job(file_data, job_data)

    tailor_data = tailor_resume(file_data, job_data, match_data)

    return {
        "resume": file_data,
        "job": job_data,
        "match": match_data,
        "matchedSkills": match_data.matched_skills,
        "missingKeywords": match_data.missing_keywords,
        "matchScore": match_data.match_score,
        "recommendations": tailor_data.recommendations,
        "tailoredResume": tailor_data.resume
    }
