import asyncio

from fastapi import APIRouter, Depends, File, Form, UploadFile

from core.rate_limit import limit_analysis
from routers.uploads import read_document, validate_job_description
from schemas.responses import ProcessCoverLetterResponse
from services.cover_letter_analyzer import analyze_cover_letter
from services.cover_letter_tailor import tailor_cover_letter
from services.job_analyzer import analyze_job
from services.matcher import match_resume_to_job

router = APIRouter()


@router.post("/process_cover_letter", response_model=ProcessCoverLetterResponse, dependencies=[Depends(limit_analysis)])
async def process_cover_letter_endpoint(
    file: UploadFile = File(...),
    job_description: str = Form(...),
    research_company: bool = Form(False),
):
    job_description = validate_job_description(job_description)
    file_text = await read_document(file)

    cover_letter, job = await asyncio.gather(analyze_cover_letter(file_text), analyze_job(job_description))

    match = await match_resume_to_job(cover_letter, job)
    tailored = await tailor_cover_letter(cover_letter, job, match, include_company_research=research_company)

    return {
        "coverLetter": cover_letter,
        "job": job,
        "match": match,
        "matchedSkills": match.matched_skills,
        "missingKeywords": match.missing_keywords,
        "matchScore": match.match_score,
        "recommendations": tailored.recommendations,
        "tailoredCoverLetter": tailored.cover_letter,
    }
