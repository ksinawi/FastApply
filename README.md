# FastApply

Tailor a resume or cover letter to a specific job posting. Upload a PDF, DOCX or TXT, paste the job description, and FastApply returns:

- a **match score** with matched and missing skills (exact plus embedding-based semantic matching)
- **recommendations** for honest additions
- an **AI-tailored rewrite** that is checked for fabricated numbers and technologies, then retried or rejected if the model invents anything
- a clean, ATS-friendly **PDF** download

Cover letters can optionally be personalized with live web research on the company.

## Stack

| Part | Tech |
|---|---|
| Frontend | Next.js 16, React 19, Tailwind CSS 4 |
| Backend | FastAPI, OpenAI (Responses API with structured outputs, embeddings), pypdf, python-docx, ReportLab |

```
backend/
  main.py              app, CORS, error handling, /health
  core/                settings (env vars), rate limiting
  routers/             HTTP endpoints and upload validation
  services/            parsing, analysis, matching, tailoring, verification, PDFs
  schemas/             Pydantic models (also used as the LLM output schemas)
  utils/               LLM + embeddings helpers, prompts
  tests/               pytest suite (uses a fake OpenAI client, no key needed)
frontend/
  app/, components/, lib/api.ts, types/
```

## Run locally

### With Docker (simplest)

```bash
cp backend/.env.example backend/.env   # then put your OPENAI_API_KEY in it
docker compose up --build
```

The frontend runs at http://localhost:3000 and the API docs at http://localhost:8000/docs.

### Without Docker

```bash
# Backend
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env                    # add OPENAI_API_KEY
uvicorn main:app --reload

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

### Tests

```bash
cd backend && pytest
cd frontend && npm run lint && npx tsc --noEmit
```

## Configuration

Backend settings come from environment variables (see `backend/.env.example`):

| Variable | Default | Purpose |
|---|---|---|
| `OPENAI_API_KEY` | (required) | OpenAI key |
| `ALLOWED_ORIGINS` | `http://localhost:3000` | Comma-separated frontend origins allowed by CORS |
| `ALLOWED_ORIGIN_REGEX` | none | Extra origins by regex, e.g. Vercel previews |
| `LLM_MODEL` / `RESEARCH_MODEL` | `gpt-4.1-mini` | Models for analysis and company research |
| `EMBEDDING_MODEL` | `text-embedding-3-small` | Model for semantic skill matching |
| `MAX_UPLOAD_MB` | `5` | Upload size limit |
| `MAX_JOB_DESCRIPTION_CHARS` | `20000` | Job description length limit |
| `RATE_LIMIT_REQUESTS` / `RATE_LIMIT_WINDOW_SECONDS` | `10` / `3600` | Analyses per IP per window (`0` disables) |

The frontend needs `NEXT_PUBLIC_API_URL`, the backend's public URL.

## Deploy (Render + Vercel)

**1. Backend on Render**
1. Push this repo to GitHub.
2. In Render, go to **New → Blueprint** and select the repo. It picks up `render.yaml` and builds `backend/Dockerfile`.
3. When prompted, set `OPENAI_API_KEY`. Set `ALLOWED_ORIGINS` to a placeholder for now; you'll update it in step 3.
4. Once deployed, check `https://<your-service>.onrender.com/health`.

**2. Frontend on Vercel**
1. In Vercel, go to **Add New → Project** and import the repo. Set **Root Directory** to `frontend`.
2. Add the environment variable `NEXT_PUBLIC_API_URL=https://<your-service>.onrender.com`.
3. Deploy.

**3. Connect them**
In Render, set `ALLOWED_ORIGINS` to your Vercel URL (e.g. `https://fastapply.vercel.app`, no trailing slash). Adjust `ALLOWED_ORIGIN_REGEX` in `render.yaml` if your Vercel project name isn't `fastapply`.

Notes:
- Render's free plan sleeps after 15 minutes of inactivity, so the first request afterwards takes about 30–60 seconds. Upgrade to a paid instance to avoid this.
- The rate limiter is in-memory, which is fine for one instance. Use Redis if you scale out.
- Set a monthly usage limit on your OpenAI account as a backstop.
