from services.llm_client import client

import json

def analyze_resume(resume_text):
    prompt = f"""
    Extract structured information from this resume.

    Return ONLY valid JSON in this format:

    {{
        "skills": [],
        "education": [],
        "experience": [],
        "projects": []
    }}

    Resume:
    {resume_text}
    """

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output_text