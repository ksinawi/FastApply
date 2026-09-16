from pydantic import BaseModel

from schemas.resume import Resume
from schemas.cover_letter import CoverLetter

class DownloadRequest(BaseModel):
    resume: Resume

class DownloadCoverLetterRequest(BaseModel):
    coverLetter: CoverLetter
