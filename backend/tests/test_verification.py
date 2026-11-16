from services.verification import find_fabricated_numbers, find_fabricated_terms, groundedness_problems

REFERENCE = "Built REST APIs with FastAPI at Acme. Improved latency by 30%."


def test_detects_invented_number():
    assert find_fabricated_numbers(REFERENCE, "Improved latency by 45%") == ["45%"]


def test_allows_existing_number():
    assert find_fabricated_numbers(REFERENCE, "Cut latency by 30%") == []


def test_detects_invented_technology():
    assert find_fabricated_terms(REFERENCE, "Built APIs with FastAPI and Kubernetes") == ["Kubernetes"]


def test_ignores_sentence_initial_words():
    assert groundedness_problems(REFERENCE, "Developed REST APIs using FastAPI.") == []
