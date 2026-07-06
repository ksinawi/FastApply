from pydantic import BaseModel

class TailoredResume(BaseModel):
    improved_bullets: list[str]
    grammar_fixed: list[str]
    recommendations: list[str]
    tailored_content: str
