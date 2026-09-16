from pydantic import BaseModel

from schemas.cover_letter import CoverLetter

class TailorCoverLetterLLMOutput(BaseModel):
    opening_paragraph: str = ""
    body_paragraphs: list[str] = []
    closing_paragraph: str = ""
    recommendations: list[str] = []

class TailoredCoverLetter(BaseModel):
    cover_letter: CoverLetter
    recommendations: list[str]
