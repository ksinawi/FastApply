from pydantic import BaseModel

from schemas.resume import Resume
from schemas.cover_letter import CoverLetter
from schemas.job import Job
from schemas.match import MatchResult

class ProcessApplicationResponse(BaseModel):
    resume: Resume
    job: Job
    match: MatchResult
    matchedSkills: list[str]
    missingKeywords: list[str]
    matchScore: float
    recommendations: list[str]
    tailoredResume: Resume

class ProcessCoverLetterResponse(BaseModel):
    coverLetter: CoverLetter
    job: Job
    match: MatchResult
    matchedSkills: list[str]
    missingKeywords: list[str]
    matchScore: float
    recommendations: list[str]
    tailoredCoverLetter: CoverLetter