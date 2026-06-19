from fastapi import UploadFile, File, APIRouter

from services.resume_parser import extract_text
from services.resume_analyzer import analyze_resume

router = APIRouter()

@router.post("/upload_resume")
async def upload_resume(file: UploadFile = File(...)):
    file_path = f"upload/{file.filename}"

    with open(file_path, "wb") as f:
        f.write(await file.read())

    resume_text = extract_text(file_path)

    analysis = analyze_resume(resume_text)

    return {
        "analysis": analysis
    }