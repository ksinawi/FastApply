from pydantic import BaseModel

from schemas.resume import Resume

class TailorLLMOutput(BaseModel):
    experience_bullets: list[list[str]] = []
    project_bullets: list[list[str]] = []
    recommendations: list[str] = []

class TailoredResume(BaseModel):
    resume: Resume
    recommendations: list[str]
