from services.llm_client import client
from schemas.resume import Resume

import json

def analyze_resume(resume_text) -> Resume:
    prompt = f"""
    You are a resume parser.

    Extract structured information from this resume.

    Do not use markdowns.
    Do not use triple backticks.
    Do not use explain anything.
    Do not write any text before or after the JSON.

    Return this EXACT shema in JSON format:


    {{
        "skills": [],
        "education": [
            {{
                "degree": "",
                "institution": "",
                "relevant_courses": [],
                "start_date": "",
                "end_date": ""
            }}
        ],
        "experience": [
            {{
                "title": "",
                "company": "",
                "start_date": "",
                "end_date": "",
                "responsibilities": []
            }}
        ],
        "projects": [
            {{
                "name": "",
                "technologies": [],
                "start_date": "",
                "end_date": "",
                "description": []
            }}
        ]
    }}

    Resume:
    {resume_text}
    """

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    data = json.loads(response.output_text)

    return Resume.model_validate(data)