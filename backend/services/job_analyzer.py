from services.llm_client import client

import json

def analyze_job(job_description):
    prompt = f"""
    You are a job analyzer.

    Extract structured information from this job description.

    Do not use markdowns.
    Do not use triple backticks.
    Do not use explain anything.
    Do not write any text before or after the JSON.

    Return this EXACT shema in JSON format:

    {{
        "job_title": "",
        "required_skills": [],
        "preferred_skills": [],
        "responsibilites": [],
        "keywords": []
    }}

    Job Description:
    {job_description}
    """

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return json.loads(response.output_text)
