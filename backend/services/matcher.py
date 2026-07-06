from schemas.match import MatchResult

def match_resume_to_job(resume, job) -> MatchResult:
    resume_skills = set(resume.skills)
    job_skills = set(job.skills)

    matched = list(resume_skills & job_skills)
    missing = list(job_skills - resume_skills)

    
    if len(matched) == len(job_skills):
        score = 100
    else:
        score = int((len(matched) / len(job_skills)) * 100)  

    if score > 80:
        fit = "high"
    elif score > 50:
        fit = "medium"
    else:
        fit = "low"

    return MatchResult(
        match_score=score,
        matched_skills=matched,
        missing_keywords=missing,
        fit_level=fit,
    )