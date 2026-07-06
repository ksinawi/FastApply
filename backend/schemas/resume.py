from pydantic import BaseModel

class Education(BaseModel):
    degree: str
    institution: str
    start_date: str
    end_date: str
    relevant_courses: list[str]

class Experience(BaseModel):
    title: str
    company: str
    start_date: str
    end_date: str
    responsibilities: list[str]

class Project(BaseModel):
    name: str
    technologies: list[str]
    start_date: str
    end_date: str
    description: list[str]

class Resume(BaseModel):
    skills: list[str]
    education: list[Education]
    experience: list[Experience]
    projects: list[Project]
