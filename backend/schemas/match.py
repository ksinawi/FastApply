from pydantic import BaseModel

class MatchResult(BaseModel):
    matched_skills: list[str]
    missing_keywords: list[str]
    match_score: float
    fit_level: str