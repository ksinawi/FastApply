from schemas.match import MatchResult
from utils.embeddings import cosine_similarity, get_embeddings

# Tuned against real text-embedding-3-small scores (see conversation): clean
# rewordings/acronym expansions cluster ~0.65-0.92, genuinely different tools
# cluster ~0.46-0.66. There is no threshold that gets everything right - short
# acronyms like "AI"/"ML" can still land just under this, and lexically close
# but different tools like "Java"/"JavaScript" can still land just over it.
# That's an inherent limit of embedding bare short tokens, not a bug to chase.
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
    """Compare job_skills against resume_skills by embedding cosine similarity.
    Returns (matched, missing). A job skill counts as matched if its best
    similarity to any resume skill clears SIMILARITY_THRESHOLD - this is what
    catches "JS" vs "JavaScript" or "Postgres" vs "PostgreSQL" that the exact
    string match above would miss."""
    if not job_skills or not resume_skills:
        return [], job_skills

    try:
        vectors = get_embeddings(resume_skills + job_skills)
    except Exception as error:
        # Semantic matching is an enhancement on top of exact matching, not a
        # dependency of it - if the embeddings call fails for any reason, fall
        # back to exact-match-only rather than failing the whole request.
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
