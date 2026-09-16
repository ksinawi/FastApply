from fastapi import APIRouter, Response

from services.pdf_generator import generate_resume_pdf
from services.cover_letter_pdf_generator import generate_cover_letter_pdf
from schemas.requests import DownloadRequest, DownloadCoverLetterRequest

router = APIRouter()

@router.post("/download")
async def download_endpoint(data: DownloadRequest):
    pdf = generate_resume_pdf(data.resume)

    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=Tailored_Resume.pdf"
        }
    )

@router.post("/download_cover_letter")
async def download_cover_letter_endpoint(data: DownloadCoverLetterRequest):
    pdf = generate_cover_letter_pdf(data.coverLetter)

    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=Tailored_Cover_Letter.pdf"
        }
    )
