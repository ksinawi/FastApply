import copy

from schemas.resume import Resume
from services.pdf_generator import _date_range, _page_count, generate_resume_pdf
from services.tailor import _prioritize_skills
from tests.conftest import RESUME


def _resume(**overrides) -> Resume:
    data = copy.deepcopy(RESUME)
    data.update(overrides)
    return Resume.model_validate(data)


def test_typical_resume_is_one_page():
    resume = _resume(skill_groups=[{"category": "Languages", "skills": ["Python"]}])
    assert _page_count(generate_resume_pdf(resume)) == 1


def test_slightly_long_resume_is_squeezed_onto_one_page():
    bullet = "Built and maintained a data pipeline in Python that processed records for analysis and reporting dashboards."
    jobs = [{"title": f"Developer {i}", "company": "Acme", "start_date": "2024", "end_date": "2025",
             "responsibilities": [bullet] * 5} for i in range(4)]
    resume = _resume(experience=jobs)
    assert _page_count(generate_resume_pdf(resume)) == 1


def test_very_long_resume_spills_to_second_page():
    bullet = "Built and maintained a data pipeline in Python that processed records for analysis and reporting dashboards."
    jobs = [{"title": f"Developer {i}", "company": "Acme", "start_date": "2024", "end_date": "2025",
             "responsibilities": [bullet] * 6} for i in range(10)]
    assert _page_count(generate_resume_pdf(_resume(experience=jobs))) == 2


def test_falls_back_to_flat_skills_without_groups():
    assert generate_resume_pdf(_resume(skill_groups=[])).startswith(b"%PDF")


def test_date_range():
    assert _date_range("Jan 2026", "Jan 2026") == "Jan 2026"
    assert _date_range("Sep 2023", "Apr 2028") == "Sep 2023 – Apr 2028"
    assert _date_range("", "2025") == "2025"


def test_job_relevant_skills_come_first():
    resume = _resume(
        skills=["Java", "React", "Python", "Docker"],
        skill_groups=[{"category": "Languages", "skills": ["Java", "Python"]},
                      {"category": "Tools", "skills": ["React", "Docker"]}],
    )
    _prioritize_skills(resume, ["python", "Docker"])
    assert resume.skills == ["Python", "Docker", "Java", "React"]
    assert resume.skill_groups[0].skills == ["Python", "Java"]
    assert resume.skill_groups[1].skills == ["Docker", "React"]
