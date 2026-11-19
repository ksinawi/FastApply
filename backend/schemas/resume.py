from pydantic import BaseModel

class ContactInfo(BaseModel):
    name: str = ""
    email: str = ""
    phone: str = ""
    location: str = ""
    links: list[str] = []

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

class SkillGroup(BaseModel):
    category: str
    skills: list[str]

class Resume(BaseModel):
    contact_info: ContactInfo
    skills: list[str]
    skill_groups: list[SkillGroup] = []
    education: list[Education]
    experience: list[Experience]
    projects: list[Project]
