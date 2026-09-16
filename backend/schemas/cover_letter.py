from pydantic import BaseModel

from schemas.resume import ContactInfo

class CoverLetter(BaseModel):
    contact_info: ContactInfo
    recipient: str = ""
    opening_paragraph: str = ""
    body_paragraphs: list[str] = []
    closing_paragraph: str = ""
    signature: str = ""
    skills: list[str] = []
