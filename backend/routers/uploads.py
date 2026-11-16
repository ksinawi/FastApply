"""Validation shared by the analysis endpoints."""
from fastapi import HTTPException, UploadFile

from core.config import settings
from services.document_parser import extract_text


async def read_document(file: UploadFile) -> str:
    """Read an uploaded document, enforcing size limits, and return its text."""
    # Read one byte past the limit so oversized uploads are rejected without buffering them fully.
    file_bytes = await file.read(settings.max_upload_bytes + 1)

    if len(file_bytes) > settings.max_upload_bytes:
        limit_mb = settings.max_upload_bytes / (1024 * 1024)
        raise HTTPException(status_code=413, detail=f"That file is too large. The limit is {limit_mb:g} MB.")

    if not file_bytes:
        raise HTTPException(status_code=400, detail="The uploaded file is empty.")

    try:
        text = extract_text(file.filename or "", file_bytes)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    if len(text) > settings.max_document_chars:
        raise HTTPException(status_code=400, detail="That document is unusually long. Please upload a resume or cover letter of a few pages at most.")

    return text


def validate_job_description(job_description: str) -> str:
    job_description = (job_description or "").strip()

    if len(job_description) < 50:
        raise HTTPException(status_code=400, detail="Please paste the full job description (at least a few sentences).")

    if len(job_description) > settings.max_job_description_chars:
        raise HTTPException(
            status_code=400,
            detail=f"The job description is too long. Please keep it under {settings.max_job_description_chars:,} characters.",
        )

    return job_description
