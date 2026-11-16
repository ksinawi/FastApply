from tests.conftest import JOB_DESCRIPTION


def _upload(text="Jane Doe\nPython developer with FastAPI and React experience."):
    return {"file": ("resume.txt", text.encode(), "text/plain")}


def test_health(api):
    assert api.get("/health").json() == {"status": "ok"}


def test_process_application(api):
    response = api.post("/process_application", files=_upload(), data={"job_description": JOB_DESCRIPTION})
    assert response.status_code == 200, response.text
    body = response.json()

    assert body["matchScore"] == 67  # Python + FastAPI of Python, FastAPI, Docker
    assert body["missingKeywords"] == ["Docker"]
    assert body["tailoredResume"]["experience"][0]["responsibilities"][0] == "Developed REST APIs using FastAPI"


def test_fabricated_bullets_are_retried_then_rejected(api, fake_llm):
    fake_llm.answers["TailorLLMOutput"] = [{
        "experience_bullets": [["Built REST APIs with FastAPI and Kubernetes", "Wrote tests for 3 services"]],
        "project_bullets": [["Built a resume tailoring tool"]],
        "recommendations": [],
    }]
    response = api.post("/process_application", files=_upload(), data={"job_description": JOB_DESCRIPTION})
    assert response.status_code == 200

    tailor_calls = [c for c in fake_llm.calls if c["text"] and c["text"]["format"]["name"] == "TailorLLMOutput"]
    assert len(tailor_calls) == 3
    assert "Kubernetes" in tailor_calls[1]["input"]  # feedback in the retry prompt
    # Original bullets are kept when the model never produces a grounded rewrite
    assert response.json()["tailoredResume"]["experience"][0]["responsibilities"][0] == "Built REST APIs with FastAPI"


def test_process_cover_letter_with_research(api, fake_llm):
    response = api.post(
        "/process_cover_letter",
        files=_upload(),
        data={"job_description": JOB_DESCRIPTION, "research_company": "true"},
    )
    assert response.status_code == 200, response.text
    assert any(call["tools"] for call in fake_llm.calls)
    assert "Globex" in response.json()["tailoredCoverLetter"]["opening_paragraph"]


def test_rejects_short_job_description(api):
    response = api.post("/process_application", files=_upload(), data={"job_description": "Python dev"})
    assert response.status_code == 400
    assert "full job description" in response.json()["detail"]


def test_rejects_large_file(api, monkeypatch):
    import routers.uploads
    from core.config import Settings

    monkeypatch.setattr(routers.uploads, "settings", Settings(max_upload_bytes=10))
    response = api.post("/process_application", files=_upload(), data={"job_description": JOB_DESCRIPTION})
    assert response.status_code == 413


def test_rejects_unsupported_file(api):
    files = {"file": ("photo.png", b"\x89PNG", "image/png")}
    response = api.post("/process_application", files=files, data={"job_description": JOB_DESCRIPTION})
    assert response.status_code == 400


def test_rate_limit(api, monkeypatch):
    from core.rate_limit import analysis_limiter

    monkeypatch.setattr(analysis_limiter, "max_requests", 2)
    for _ in range(2):
        assert api.post("/process_application", files=_upload(), data={"job_description": JOB_DESCRIPTION}).status_code == 200

    response = api.post("/process_application", files=_upload(), data={"job_description": JOB_DESCRIPTION})
    assert response.status_code == 429
    assert "Retry-After" in response.headers


def test_cors_headers_on_errors(api):
    response = api.post(
        "/process_application",
        files=_upload(),
        data={"job_description": "short"},
        headers={"Origin": "http://localhost:3000"},
    )
    assert response.status_code == 400
    assert response.headers["access-control-allow-origin"] == "http://localhost:3000"


def test_download_pdfs(api):
    from tests.conftest import COVER_LETTER, RESUME

    resume_pdf = api.post("/download", json={"resume": RESUME})
    letter_pdf = api.post("/download_cover_letter", json={"coverLetter": COVER_LETTER})
    for response in (resume_pdf, letter_pdf):
        assert response.status_code == 200
        assert response.content.startswith(b"%PDF")
