from schemas.cover_letter import CoverLetter
from utils.llm import call_llm
from utils.prompts import COVER_LETTER_ANALYZER_PROMPT


async def analyze_cover_letter(cover_letter_text: str) -> CoverLetter:
    return await call_llm(COVER_LETTER_ANALYZER_PROMPT.format(cover_letter=cover_letter_text), CoverLetter)
