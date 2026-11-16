import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from core.config import settings
from routers import download_router, process_application_router, process_cover_letter_router

logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("fastapply")

if not settings.openai_api_key:
    logger.warning("OPENAI_API_KEY is not set; analysis requests will fail.")

app = FastAPI(title="FastApply API", version="1.0.0")

@app.middleware("http")
async def catch_unhandled_errors(request: Request, call_next):
    # Registered before CORS so CORS wraps it: error responses still carry CORS headers
    # and the browser can show the message instead of an opaque network error.
    try:
        return await call_next(request)
    except Exception:
        logger.exception("Unhandled error on %s %s", request.method, request.url.path)
        return JSONResponse(status_code=500, content={"detail": "Something went wrong on our end. Please try again."})


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_origin_regex=settings.allowed_origin_regex,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/health", tags=["meta"])
async def health():
    return {"status": "ok"}


app.include_router(process_application_router.router)
app.include_router(process_cover_letter_router.router)
app.include_router(download_router.router)
