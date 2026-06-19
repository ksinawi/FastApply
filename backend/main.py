from fastapi import FastAPI

from routers import resume_router
from routers import job_router
from routers import match_router

app = FastAPI()

app.include_router(resume_router.router)
app.include_router(job_router.router)
app.include_router(match_router.router)
