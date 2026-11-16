import asyncio

from fastapi import APIRouter, Depends, File, Form, UploadFile

from core.rate_limit import limit_analysis
from routers.uploads import read_document, validate_job_description
from schemas.responses import ProcessApplicationResponse
from services.job_analyzer import analyze_job
from services.matcher import match_resume_to_job
from services.resume_analyzer import analyze_resume
from services.tailor import tailor_resume

router = APIRouter()


@router.post("/process_application", response_model=ProcessApplicationResponse, dependencies=[Depends(limit_analysis)])
async def process_application_endpoint(file: UploadFile = File(...), job_description: str = Form(...)):
    job_description = validate_job_description(job_description)
    file_text = await read_document(file)

    # Parsing the resume and the job posting are independent, so run them together.
    resume, job = await asyncio.gather(analyze_resume(file_text), analyze_job(job_description))

    match = await match_resume_to_job(resume, job)
    tailored = await tailor_resume(resume, job, match)

    return {
        "resume": resume,
        "job": job,
        "match": match,
        "matchedSkills": match.matched_skills,
        "missingKeywords": match.missing_keywords,
        "matchScore": match.match_score,
        "recommendations": tailored.recommendations,
        "tailoredResume": tailored.resume,
    }
