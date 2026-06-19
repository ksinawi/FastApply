from services.llm_client import client

import json

def tailor_resume(resume, job, match):
    prompt = f"""
    Your goal is to improve the resume. 

    You are NOT allowed to invent skills, tools, or experiences.

    Only use information explicitly present in the resume.

    If something is missing, return it as a recommendation only.
    Never add it to resume content.
    
    CRITICAL RULES:
    - Do NOT invent skills, tools, or experience.
    - ONLY use information present in the resume.
    - If something is missing, put it under "recommendations", NOT the resume.
    - Do not include explanations or commentary.

    {{
        "improved_bullets": [],
        "grammar_fixed": [],
        "recommendations": [],
        "warnings: []
    }}

    Resume: {resume}
    Job: {job}
    Match: {match}
    """

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return json.loads(response.output_text)