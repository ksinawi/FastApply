from fastapi import APIRouter, Response

from services.pdf_generator import generate_resume_pdf
from schemas.requests import DownloadRequest

router = APIRouter()

@router.post("/download")
async def download_endpoint(data: DownloadRequest):
    pdf = generate_resume_pdf(data.tailoredContent)

    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=Tailored_Resume.pdf"
        }
    )
