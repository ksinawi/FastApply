import json
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

RESUME = {
    "contact_info": {"name": "Jane Doe", "email": "jane@example.com", "phone": "", "location": "Toronto, ON", "links": []},
    "skills": ["Python", "FastAPI", "React"],
    "education": [{"degree": "BSc Computer Science", "institution": "University of Guelph", "start_date": "2021", "end_date": "2025", "relevant_courses": []}],
    "experience": [{"title": "Developer Intern", "company": "Acme", "start_date": "May 2024", "end_date": "Aug 2024",
                    "responsibilities": ["Built REST APIs with FastAPI", "Wrote tests for 3 services"]}],
    "projects": [{"name": "FastApply", "technologies": ["Python", "React"], "start_date": "", "end_date": "", "description": ["Built a resume tailoring tool"]}],
}
COVER_LETTER = {
    "contact_info": {"name": "Jane Doe", "email": "jane@example.com", "phone": "", "location": "", "links": []},
    "recipient": "Dear Hiring Manager,",
    "opening_paragraph": "I am excited to apply to Globex.",
    "body_paragraphs": ["At Acme I built REST APIs with Python."],
    "closing_paragraph": "Thank you for your time.",
    "signature": "Sincerely, Jane Doe",
    "skills": ["Python"],
}
JOB = {"title": "Backend Engineer", "company": "Globex", "skills": ["Python", "FastAPI", "Docker"],
       "responsibilities": ["Build APIs"], "keywords": ["APIs"], "qualifications": []}

JOB_DESCRIPTION = "Globex is hiring a Backend Engineer. You will build APIs in Python and FastAPI, and ship with Docker."


class FakeResponses:
    def __init__(self, client):
        self.client = client

    async def create(self, model, input, text=None, tools=None):
        self.client.calls.append({"input": input, "text": text, "tools": tools})

        if tools:  # company research
            return SimpleNamespace(status="completed", output_text="- Globex builds rockets.", incomplete_details=None)

        name = text["format"]["name"]
        payload = self.client.answers[name]
        if isinstance(payload, list):  # successive answers for retries
            payload = payload.pop(0) if len(payload) > 1 else payload[0]

        return SimpleNamespace(status="completed", output_text=json.dumps(payload), incomplete_details=None)


class FakeEmbeddings:
    async def create(self, model, input):
        # Identical strings get identical vectors; everything else is orthogonal-ish.
        vocab = {}
        data = []
        for index, text in enumerate(input):
            key = text.lower()
            vocab.setdefault(key, len(vocab))
            vector = [0.0] * 64
            vector[vocab[key] % 64] = 1.0
            data.append(SimpleNamespace(index=index, embedding=vector))
        return SimpleNamespace(data=data)


class FakeClient:
    def __init__(self):
        self.calls = []
        self.answers = {
            "Resume": RESUME,
            "CoverLetter": COVER_LETTER,
            "Job": JOB,
            "TailorLLMOutput": {
                "experience_bullets": [["Developed REST APIs using FastAPI", "Wrote automated tests for 3 services"]],
                "project_bullets": [["Built a resume tailoring tool with Python and React"]],
                "recommendations": ["Mention Docker experience if you have used it."],
            },
            "TailorCoverLetterLLMOutput": {
                "opening_paragraph": "I am excited to apply for the Backend Engineer role at Globex.",
                "body_paragraphs": ["At Acme I built REST APIs with Python."],
                "closing_paragraph": "Thank you for your time and consideration.",
                "recommendations": [],
            },
        }
        self.responses = FakeResponses(self)
        self.embeddings = FakeEmbeddings()


@pytest.fixture
def fake_llm(monkeypatch):
    client = FakeClient()
    for module in ("utils.llm", "utils.embeddings", "services.company_research"):
        monkeypatch.setattr(f"{module}.get_client", lambda: client)
    return client


@pytest.fixture
def api(fake_llm):
    from core.rate_limit import analysis_limiter
    from main import app

    analysis_limiter.reset()
    return TestClient(app)
