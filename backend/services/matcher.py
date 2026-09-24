from schemas.match import MatchResult
from utils.embeddings import cosine_similarity, get_embeddings

SIMILARITY_THRESHOLD = 0.65

def match_resume_to_job(resume, job) -> MatchResult:
    resume_skills = resume.skills
    job_skills = job.skills

    if not job_skills:
        return MatchResult(match_score=100, matched_skills=[], missing_keywords=[], fit_level="high")

    resume_lookup = {skill.lower() for skill in resume_skills}

    exact_matched = [skill for skill in job_skills if skill.lower() in resume_lookup]
    unmatched = [skill for skill in job_skills if skill.lower() not in resume_lookup]

    soft_matched, missing = _semantic_match(resume_skills, unmatched)

    matched = exact_matched + soft_matched
    score = round(len(matched) / len(job_skills) * 100)

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

def _semantic_match(resume_skills: list[str], job_skills: list[str]) -> tuple[list[str], list[str]]:
    if not job_skills or not resume_skills:
        return [], job_skills

    try:
        vectors = get_embeddings(resume_skills + job_skills)
    except Exception as error:
        print(f"[matcher] semantic matching unavailable, falling back to exact matches only: {error}")
        return [], job_skills

    resume_vectors = vectors[:len(resume_skills)]
    job_vectors = vectors[len(resume_skills):]

    matched = []
    missing = []

    for job_skill, job_vector in zip(job_skills, job_vectors):
        best_similarity = max(cosine_similarity(job_vector, resume_vector) for resume_vector in resume_vectors)

        if best_similarity >= SIMILARITY_THRESHOLD:
            matched.append(job_skill)
        else:
            missing.append(job_skill)

    return matched, missing
