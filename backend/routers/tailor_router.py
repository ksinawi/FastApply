from fastapi import APIRouter
from pydantic import BaseModel

from services.tailor import tailor_resume

class TailorRequest(BaseModel):
    resume: dict
    job: dict
    match: dict

router = APIRouter()

@router.post("/tailor")
def tailor_endpoint(data: TailorRequest):
    resume = data.resume
    job = data.job
    match = data.match

    result = tailor_resume(resume, job, match)

    return result
