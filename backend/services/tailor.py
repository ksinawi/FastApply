from schemas.resume import Resume
from schemas.tailored import TailoredResume, TailorLLMOutput
from utils.prompts import TAILOR_PROMPT
from utils.llm import call_llm

def _merged_bullets(original: list[str], improved: list[str]) -> list[str]:
    cleaned = [b.strip() for b in improved if b and b.strip()]

    if len(cleaned) != len(original):
        return original

    return cleaned

def tailor_resume(resume: Resume, job, match) -> TailoredResume:
    prompt = TAILOR_PROMPT.format(
        structured_resume=resume.model_dump_json(indent=2),
        job=job.model_dump_json(indent=2),
        match=match.model_dump_json(indent=2),
    )

    data = call_llm(prompt)
    llm_output = TailorLLMOutput.model_validate(data)

    tailored = resume.model_copy(deep=True)

    for experience, bullets in zip(tailored.experience, llm_output.experience_bullets):
        experience.responsibilities = _merged_bullets(experience.responsibilities, bullets)

    for project, bullets in zip(tailored.projects, llm_output.project_bullets):
        project.description = _merged_bullets(project.description, bullets)

    return TailoredResume(resume=tailored, recommendations=llm_output.recommendations)
