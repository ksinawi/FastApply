from services.llm_client import client
from schemas.job import Job

import json

def analyze_job(job_description) -> Job:
    prompt = f"""
    You are a job analyzer.

    Extract structured information from this job description.

    Do not use markdowns.
    Do not use triple backticks.
    Do not use explain anything.
    Do not write any text before or after the JSON.

    Return STRICT JSON ONLY.

    Skills must be atomic technical keywords.

    BAD:
    "Knowledge in Java, JavaScript, Python"

    GOOD:
    ["Java", "JavaScript", "Python"]

    If unsure, extract individual technologies only.

    Return this EXACT shema in JSON format:

    {{
        "title": "",
        "company": "",
        "skills": [],
        "responsibilities": [],
        "keywords": [],
        "qualifications": []
    }}

    Job Description:
    {job_description}
    """

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    data = json.loads(response.output_text)

    return Job.model_validate(data)
