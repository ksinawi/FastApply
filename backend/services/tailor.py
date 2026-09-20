from schemas.resume import Resume
from schemas.tailored import TailoredResume, TailorLLMOutput
from services.verification import call_llm_with_verification, groundedness_problems
from utils.prompts import TAILOR_PROMPT

MAX_VERIFICATION_ATTEMPTS = 3

def _merged_bullets(original: list[str], improved: list[str]) -> list[str]:
    cleaned = [b.strip() for b in improved if b and b.strip()]

    if len(cleaned) != len(original):
        return original

    return cleaned

def _reference_text(resume: Resume) -> str:
    parts = list(resume.skills)

    for experience in resume.experience:
        parts += [experience.title, experience.company, *experience.responsibilities]

    for project in resume.projects:
        parts += [project.name, *project.technologies, *project.description]

    for education in resume.education:
        parts += [education.degree, education.institution, *education.relevant_courses]

    return " ".join(part for part in parts if part)

def _verify(reference_text: str, llm_output: TailorLLMOutput) -> list[str]:
    problems = []

    for exp_index, bullets in enumerate(llm_output.experience_bullets):
        for bullet_index, bullet in enumerate(bullets):
            for problem in groundedness_problems(reference_text, bullet):
                problems.append(f'experience_bullets[{exp_index}][{bullet_index}] {problem}: "{bullet}"')

    for proj_index, bullets in enumerate(llm_output.project_bullets):
        for bullet_index, bullet in enumerate(bullets):
            for problem in groundedness_problems(reference_text, bullet):
                problems.append(f'project_bullets[{proj_index}][{bullet_index}] {problem}: "{bullet}"')

    return problems

def tailor_resume(resume: Resume, job, match) -> TailoredResume:
    reference_text = _reference_text(resume)

    prompt = TAILOR_PROMPT.format(
        structured_resume=resume.model_dump_json(indent=2),
        job=job.model_dump_json(indent=2),
        match=match.model_dump_json(indent=2),
    )

    llm_output, verified = call_llm_with_verification(
        base_prompt=prompt,
        response_model=TailorLLMOutput,
        verify=lambda output: _verify(reference_text, output),
        max_attempts=MAX_VERIFICATION_ATTEMPTS,
    )

    if not verified:
        print("[tailor_resume] giving up after failed verification, keeping original bullets")
        llm_output = TailorLLMOutput(recommendations=llm_output.recommendations)

    tailored = resume.model_copy(deep=True)

    for experience, bullets in zip(tailored.experience, llm_output.experience_bullets):
        experience.responsibilities = _merged_bullets(experience.responsibilities, bullets)

    for project, bullets in zip(tailored.projects, llm_output.project_bullets):
        project.description = _merged_bullets(project.description, bullets)

    return TailoredResume(resume=tailored, recommendations=llm_output.recommendations)
