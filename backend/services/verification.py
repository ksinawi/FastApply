import logging
import re

from utils.llm import call_llm

logger = logging.getLogger(__name__)

NUMBER_PATTERN = re.compile(r"\d+(?:\.\d+)?%?")
CAPITALIZED_WORD_PATTERN = re.compile(r"[A-Z][a-zA-Z0-9+.#/-]*")

COMMON_CAPITALIZED_WORDS = {
    "I", "I'm", "I'll", "I've", "I'd",
    "A", "An", "The", "This", "That", "These", "Those",
    "In", "On", "At", "To", "For", "With", "And", "Or", "But", "By", "As",
    "Of", "From", "Into", "Onto", "Over", "Under", "Through", "During",
    "Is", "Are", "Was", "Were", "Be", "Been", "Being",
    "My", "Our", "Their", "His", "Her", "Its", "Your",
}


def extract_numbers(text: str) -> set[str]:
    return set(NUMBER_PATTERN.findall(text or ""))


def extract_capitalized_terms(text: str) -> set[str]:
    terms = set()

    for sentence in re.split(r"(?<=[.!?])\s+", (text or "").strip()):
        words = sentence.split()

        for index, raw_word in enumerate(words):
            word = raw_word.strip("\"'’,.;:()[]")

            if not word or index == 0 or word in COMMON_CAPITALIZED_WORDS:
                continue

            if CAPITALIZED_WORD_PATTERN.fullmatch(word):
                terms.add(word)

    return terms


def find_fabricated_numbers(reference_text: str, candidate_text: str) -> list[str]:
    candidate_numbers = extract_numbers(candidate_text)
    reference_numbers = extract_numbers(reference_text)

    return sorted(candidate_numbers - reference_numbers)


def find_fabricated_terms(reference_text: str, candidate_text: str) -> list[str]:
    candidate_terms = extract_capitalized_terms(candidate_text)
    reference_lower = (reference_text or "").lower()

    fabricated = []

    for term in sorted(candidate_terms):
        pattern = r"\b" + re.escape(term.lower()) + r"\b"
        if not re.search(pattern, reference_lower):
            fabricated.append(term)

    return fabricated


def groundedness_problems(reference_text: str, candidate_text: str) -> list[str]:
    """All groundedness problems found in candidate_text, as readable strings."""
    problems = []

    numbers = find_fabricated_numbers(reference_text, candidate_text)
    if numbers:
        problems.append(f"introduces number(s) not present in the original: {', '.join(numbers)}")

    terms = find_fabricated_terms(reference_text, candidate_text)
    if terms:
        problems.append(f"introduces term(s) not present in the original: {', '.join(terms)}")

    return problems


def build_retry_prompt(base_prompt: str, problems: list[str]) -> str:
    feedback = "\n".join(f"- {problem}" for problem in problems)

    return (
        base_prompt
        + "\n\nYour previous answer violated the rules above. Specifically:\n"
        + feedback
        + "\n\nReturn a corrected JSON response that fixes these issues without introducing new ones. "
        + "Only use skills, technologies, and facts already present in the structured input above."
    )


async def call_llm_with_verification(base_prompt, response_model, verify, max_attempts=3):
    problems: list[str] = []
    output = None

    for attempt in range(max_attempts):
        prompt = base_prompt if attempt == 0 else build_retry_prompt(base_prompt, problems)

        output = await call_llm(prompt, response_model)

        problems = verify(output)
        if not problems:
            return output, True

        logger.info("Verification attempt %d/%d failed: %s", attempt + 1, max_attempts, problems)

    return output, False
