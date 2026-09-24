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
- If a field or date is unknown, return an empty string.
- Extract ALL skills that appear anywhere in the resume.
- Extract the candidate's name, email, phone, location, and any links (LinkedIn, GitHub, portfolio, personal site) from the resume header.

Return this exact JSON schema:

{{
    "contact_info": {{
        "name": "",
        "email": "",
        "phone": "",
        "location": "",
        "links": []
    }},
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

COVER_LETTER_ANALYZER_PROMPT = """
You are an expert cover letter parser.

Your task is to extract structured information from a cover letter.

Rules:
- Return ONLY valid JSON.
- Do NOT use markdown.
- Do NOT use triple backticks.
- Do NOT explain your reasoning.
- Do NOT invent information.
- Preserve the wording from the letter whenever possible.
- If a field is missing, return an empty string or empty list as appropriate.
- Extract the candidate's name, email, phone, location, and any links from the header/signature.
- "recipient" is the greeting line (e.g. "Dear Hiring Manager," or "Dear Ms. Smith,"). If none is
  present, use "Dear Hiring Manager,".
- "opening_paragraph" is the first paragraph of the letter body (after the greeting).
- "body_paragraphs" is every paragraph between the opening and closing paragraph, in order, as a list.
  If there is only one body paragraph total, treat it as the opening_paragraph and return an empty list here.
- "closing_paragraph" is the final paragraph before the sign-off.
- "signature" is the sign-off phrase plus name (e.g. "Sincerely, Jane Doe"). If none is present, use
  "Sincerely," followed by the candidate's name.
- "skills" lists every skill, technology, or qualification explicitly mentioned anywhere in the letter.

Return this exact JSON schema:

{{
    "contact_info": {{
        "name": "",
        "email": "",
        "phone": "",
        "location": "",
        "links": []
    }},
    "recipient": "",
    "opening_paragraph": "",
    "body_paragraphs": [],
    "closing_paragraph": "",
    "signature": "",
    "skills": []
}}

Cover Letter:

{cover_letter}
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

Your ONLY job is to rewrite the bullet points listed in the Structured Resume below so they
are stronger and better aligned with the target job, while remaining completely truthful.
You are NOT rewriting the resume itself — layout, headings, section order, dates, skills,
and education are handled elsewhere in code and are none of your concern.

STRICT RULES

You MUST NOT:
- Invent skills, technologies, certifications, projects, or measurable achievements.
- Invent or change years of experience, employment dates, or education.
- Add a bullet point, remove a bullet point, merge bullet points, or reorder bullet points.
- Change the number of items in any list you return. Every array you return MUST have
  exactly the same length, in the same order, as the corresponding entry below.

You MAY, for each existing bullet point individually:
- Improve wording, grammar, and clarity.
- Use stronger, more specific action verbs.
- Improve ATS keyword placement using ONLY skills/technologies already present elsewhere
  in the Structured Resume.

If the job requires something the candidate does NOT have, do NOT add it to a bullet.
Instead, note it under recommendations as something the user could honestly add if it is
true but missing from the resume (e.g. "Mention Docker experience if you have used it.").

Never fabricate information.

Return ONLY valid JSON with this exact schema:

{{
    "experience_bullets": [[]],
    "project_bullets": [[]],
    "recommendations": []
}}

Where:
- "experience_bullets" contains exactly one array per entry in "experience" below, in the
  same order, each holding the rewritten "responsibilities" for that entry — same length
  as the original.
- "project_bullets" contains exactly one array per entry in "projects" below, in the same
  order, each holding the rewritten "description" for that entry — same length as the
  original.
- If "experience" or "projects" is empty, return an empty list for that field.

Structured Resume:

{structured_resume}

Job:

{job}

Match Results:

{match}
"""

TAILOR_COVER_LETTER_PROMPT = """
You are a professional cover letter writer.

Your ONLY job is to rewrite the paragraphs of the cover letter below so it reads more
persuasively and aligns better with the target job, while remaining completely truthful.
You are NOT changing the greeting or signature — those are handled elsewhere in code and
are none of your concern.

STRICT RULES

You MUST NOT:
- Invent skills, experience, achievements, companies, or qualifications that are not
  already present in the Structured Cover Letter below.
- Invent or change names, dates, or job titles.
- Add a new paragraph or remove a paragraph. You MUST return exactly one
  opening_paragraph, exactly one closing_paragraph, and a body_paragraphs list with
  exactly the same number of items, in the same order, as the "body_paragraphs" field
  below.

You MAY, for each paragraph individually:
- Improve wording, tone, grammar, and clarity.
- Make the pitch more persuasive using only what is already true.
- Improve keyword alignment with the job posting using ONLY skills/experience already
  present in the Structured Cover Letter.
- Reference a fact from the "Company Research" section below, if it is non-empty, to
  personalize the opening or closing paragraph (e.g. tying the candidate's interest to
  the company's mission or a recent announcement). If that section is empty, do not
  mention it or make anything up in its place.

If the job wants something the candidate does NOT mention, do NOT fabricate it into the
letter. Instead, note it under recommendations as something the user could honestly add
if it is true but missing.

Return ONLY valid JSON with this exact schema:

{{
    "opening_paragraph": "",
    "body_paragraphs": [],
    "closing_paragraph": "",
    "recommendations": []
}}

Structured Cover Letter:

{structured_cover_letter}

Job:

{job}

Match Results:

{match}

Company Research (optional - only use if non-empty, never invent facts beyond it):

{company_research}
"""

COMPANY_RESEARCH_PROMPT = """
You are researching a company on behalf of someone about to write a personalized cover
letter to them.

Search the web for a few genuinely useful, CURRENT facts about "{company}" that would
help personalize a cover letter for a "{job_title}" role there - for example their
mission or values, a recent product launch or news item, or something distinctive about
their culture or work.

Rules:
- Only include facts you are reasonably confident are accurate and about THIS specific
  company, not a similarly-named one.
- If you cannot find reliable, specific information about this company, say so plainly
  instead of guessing or generalizing.
- Keep it to 2-4 short factual bullet points, plain text, no markdown formatting.
- Do not invent facts.

Company: {company}
Role: {job_title}
"""