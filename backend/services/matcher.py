
def match_resume_to_job(resume, job):
    resume_skills = set(resume["skills"])
    job_skills = set(job["required_skills"])

    matched = list(resume_skills & job_skills)
    missing = list(job_skills - resume_skills)

    score = int(len(matched) / len(missing) * 100)  

    if score > 80:
        fit = "high"
    elif score > 50:
        fit = "medium"
    else:
        fit = "low"

    return {
        "match-score": score,
        "matched_skills": matched,
        "missin-skills": missing,
        "fit_level": fit
    }