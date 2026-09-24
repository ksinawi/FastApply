from schemas.cover_letter import CoverLetter
from schemas.tailored_cover_letter import TailoredCoverLetter, TailorCoverLetterLLMOutput
from services.company_research import research_company
from services.verification import call_llm_with_verification, groundedness_problems
from utils.prompts import TAILOR_COVER_LETTER_PROMPT

MAX_VERIFICATION_ATTEMPTS = 3

def _merged_paragraph(original: str, improved: str) -> str:
    return improved.strip() if improved and improved.strip() else original

def _merged_paragraphs(original: list[str], improved: list[str]) -> list[str]:
    cleaned = [p.strip() for p in improved if p and p.strip()]

    if len(cleaned) != len(original):
        return original

    return cleaned

def _reference_text(cover_letter: CoverLetter, job, company_research: str) -> str:
    parts = [
        job.company,
        job.title,
        company_research,
        *cover_letter.skills,
        cover_letter.opening_paragraph,
        *cover_letter.body_paragraphs,
        cover_letter.closing_paragraph,
    ]

    return " ".join(part for part in parts if part)

def _verify(reference_text: str, llm_output: TailorCoverLetterLLMOutput) -> list[str]:
    problems = []

    for problem in groundedness_problems(reference_text, llm_output.opening_paragraph):
        problems.append(f"opening_paragraph {problem}")

    for index, paragraph in enumerate(llm_output.body_paragraphs):
        for problem in groundedness_problems(reference_text, paragraph):
            problems.append(f"body_paragraphs[{index}] {problem}")

    for problem in groundedness_problems(reference_text, llm_output.closing_paragraph):
        problems.append(f"closing_paragraph {problem}")

    return problems

def tailor_cover_letter(cover_letter: CoverLetter, job, match, include_company_research: bool = False) -> TailoredCoverLetter:
    company_research = research_company(job.company, job.title) if include_company_research else ""

    reference_text = _reference_text(cover_letter, job, company_research)

    prompt = TAILOR_COVER_LETTER_PROMPT.format(
        structured_cover_letter=cover_letter.model_dump_json(indent=2),
        job=job.model_dump_json(indent=2),
        match=match.model_dump_json(indent=2),
        company_research=company_research or "(none)",
    )

    llm_output, verified = call_llm_with_verification(
        base_prompt=prompt,
        response_model=TailorCoverLetterLLMOutput,
        verify=lambda output: _verify(reference_text, output),
        max_attempts=MAX_VERIFICATION_ATTEMPTS,
    )

    if not verified:
        print("[tailor_cover_letter] giving up after failed verification, keeping original paragraphs")
        llm_output = TailorCoverLetterLLMOutput(recommendations=llm_output.recommendations)

    tailored = cover_letter.model_copy(deep=True)
    tailored.opening_paragraph = _merged_paragraph(cover_letter.opening_paragraph, llm_output.opening_paragraph)
    tailored.body_paragraphs = _merged_paragraphs(cover_letter.body_paragraphs, llm_output.body_paragraphs)
    tailored.closing_paragraph = _merged_paragraph(cover_letter.closing_paragraph, llm_output.closing_paragraph)

    return TailoredCoverLetter(cover_letter=tailored, recommendations=llm_output.recommendations)
