from schemas.cover_letter import CoverLetter
from schemas.tailored_cover_letter import TailoredCoverLetter, TailorCoverLetterLLMOutput
from utils.prompts import TAILOR_COVER_LETTER_PROMPT
from utils.llm import call_llm

def _merged_paragraph(original: str, improved: str) -> str:
    return improved.strip() if improved and improved.strip() else original

def _merged_paragraphs(original: list[str], improved: list[str]) -> list[str]:
    cleaned = [p.strip() for p in improved if p and p.strip()]

    if len(cleaned) != len(original):
        return original

    return cleaned

def tailor_cover_letter(cover_letter: CoverLetter, job, match) -> TailoredCoverLetter:
    prompt = TAILOR_COVER_LETTER_PROMPT.format(
        structured_cover_letter=cover_letter.model_dump_json(indent=2),
        job=job.model_dump_json(indent=2),
        match=match.model_dump_json(indent=2),
    )

    data = call_llm(prompt)
    llm_output = TailorCoverLetterLLMOutput.model_validate(data)

    tailored = cover_letter.model_copy(deep=True)
    tailored.opening_paragraph = _merged_paragraph(cover_letter.opening_paragraph, llm_output.opening_paragraph)
    tailored.body_paragraphs = _merged_paragraphs(cover_letter.body_paragraphs, llm_output.body_paragraphs)
    tailored.closing_paragraph = _merged_paragraph(cover_letter.closing_paragraph, llm_output.closing_paragraph)

    return TailoredCoverLetter(cover_letter=tailored, recommendations=llm_output.recommendations)
