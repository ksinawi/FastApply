import json

from schemas.cover_letter import CoverLetter
from schemas.job import Job
from utils.llm import response_format


def test_schema_is_strict_mode_compatible():
    for model in (CoverLetter, Job):
        schema = response_format(model)
        dumped = json.dumps(schema)
        assert schema["strict"] is True
        assert '"default"' not in dumped
        assert schema["schema"]["additionalProperties"] is False


def test_field_named_title_is_kept():
    assert "title" in response_format(Job)["schema"]["properties"]
