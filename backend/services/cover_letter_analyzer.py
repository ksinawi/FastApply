from schemas.cover_letter import CoverLetter
from utils.prompts import COVER_LETTER_ANALYZER_PROMPT
from utils.llm import call_llm

def analyze_cover_letter(cover_letter_text) -> CoverLetter:
    prompt = COVER_LETTER_ANALYZER_PROMPT.format(cover_letter=cover_letter_text)

    data = call_llm(prompt)

    return CoverLetter.model_validate(data)
