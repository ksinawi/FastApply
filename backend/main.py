from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import process_application_router
from routers import process_cover_letter_router
from routers import download_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(process_application_router.router)
app.include_router(process_cover_letter_router.router)
app.include_router(download_router.router)
