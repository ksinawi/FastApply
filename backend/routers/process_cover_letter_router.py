from fastapi import APIRouter, HTTPException, UploadFile, File, Form

from services.document_parser import extract_text
from services.cover_letter_analyzer import analyze_cover_letter
from services.job_analyzer import analyze_job
from services.matcher import match_resume_to_job
from services.cover_letter_tailor import tailor_cover_letter

from schemas.responses import ProcessCoverLetterResponse

router = APIRouter()

@router.post("/process_cover_letter", response_model=ProcessCoverLetterResponse)
async def process_cover_letter_endpoint(
    file: UploadFile = File(...),
    job_description: str = Form(...),
    research_company: bool = Form(False),
):

    file_bytes = await file.read()

    try:
        file_text = extract_text(file.filename, file_bytes)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    cover_letter_data = analyze_cover_letter(file_text)
    job_data = analyze_job(job_description)

    match_data = match_resume_to_job(cover_letter_data, job_data)

    tailor_data = tailor_cover_letter(cover_letter_data, job_data, match_data, include_company_research=research_company)

    return {
        "coverLetter": cover_letter_data,
        "job": job_data,
        "match": match_data,
        "matchedSkills": match_data.matched_skills,
        "missingKeywords": match_data.missing_keywords,
        "matchScore": match_data.match_score,
        "recommendations": tailor_data.recommendations,
        "tailoredCoverLetter": tailor_data.cover_letter
    }
