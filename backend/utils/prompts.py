RESUME_ANALYZER_PROMPT = """
You are an expert resume parser.

Your task is to extract structured information from a resume.

Rules:
- Return ONLY valid JSON.
- Do NOT use markdown.
- Do NOT use triple backticks.
- Do NOT explain your reasoning.
- Do NOT invent information.
- Preserve the wording from the resume whenever possible.
- If a section is missing, return an empty list.
- If a date is unknown, return an empty string.
- Extract ALL skills that appear anywhere in the resume.

Return this exact JSON schema:

{{
    "skills": [],
    "education": [
        {{
            "degree": "",
            "institution": "",
            "start_date": "",
            "end_date": "",
            "relevant_courses": []
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

{resume}
"""

JOB_ANALYZER_PROMPT = """
You are an expert technical recruiter.

Analyze the job posting and extract ONLY information explicitly stated.

Rules:
- Return ONLY valid JSON.
- Do NOT use markdown.
- Do NOT explain anything.
- Do NOT infer missing information.
- Do NOT invent requirements.
- Keep wording close to the original posting.
- Separate required skills from preferred skills whenever possible.
- Extract ATS keywords that are important for ranking.

Return this exact JSON schema:

{{
    "title": "",
    "company": "",
    "skills": [],
    "responsibilities": [],
    "keywords": [],
    "qualifications": []
}}

Job Description:

{job}
"""

TAILOR_PROMPT = """
You are a professional resume writer specializing in ATS optimization.

Your objective is to improve the resume while remaining completely truthful.

STRICT RULES

You MUST NOT:
- Invent skills.
- Invent technologies.
- Invent certifications.
- Invent projects.
- Invent responsibilities.
- Invent measurable achievements.
- Invent years of experience.
- Change employment dates.
- Change education.
- Add experience that is not present.

You MAY:
- Rewrite bullet points.
- Improve grammar.
- Improve clarity.
- Improve wording.
- Reorder bullet points.
- Emphasize existing technologies.
- Use stronger action verbs.
- Improve ATS keyword placement using ONLY existing experience.
- Merge similar bullet points.
- Remove redundancy.

If the job requires something the candidate does NOT have:

DO NOT add it.

Instead, place it under recommendations.

Your recommendations should tell the user what they could honestly add if it is true but missing from the resume.

Examples:
- Mention Docker experience if you have used it.
- Include your AWS certification if applicable.
- Add your GitHub portfolio.

Never fabricate information.

Return ONLY valid JSON.

{{
    "improved_bullets": [],
    "grammar_fixed": [],
    "recommendations": [],
    "tailored_content": ""
}}

Resume:

{resume}

Job:

{job}

Match Results:

{match}
"""