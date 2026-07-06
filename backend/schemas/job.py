from pydantic import BaseModel

class Job(BaseModel):
    title: str
    company: str
    skills: list[str]
    responsibilities: list[str]
    keywords: list[str]
    qualifications: list[str]