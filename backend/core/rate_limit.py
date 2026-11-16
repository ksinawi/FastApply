"""A small in-memory, per-IP sliding-window rate limiter.

Good enough for a single backend instance (e.g. one Render service). If you scale to
several instances, move this to a shared store such as Redis.
"""
import time
from collections import defaultdict, deque

from fastapi import HTTPException, Request

from core.config import settings


class RateLimiter:
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._hits: dict[str, deque[float]] = defaultdict(deque)

    def check(self, key: str) -> None:
        if self.max_requests <= 0:
            return

        now = time.monotonic()
        hits = self._hits[key]

        while hits and now - hits[0] > self.window_seconds:
            hits.popleft()

        if len(hits) >= self.max_requests:
            retry_after = int(self.window_seconds - (now - hits[0])) + 1
            raise HTTPException(
                status_code=429,
                detail=f"You've reached the limit of {self.max_requests} analyses. Please try again in {_human(retry_after)}.",
                headers={"Retry-After": str(retry_after)},
            )

        hits.append(now)

    def reset(self) -> None:
        self._hits.clear()


def _human(seconds: int) -> str:
    if seconds < 60:
        return f"{seconds} seconds"
    minutes = round(seconds / 60)
    return f"{minutes} minute{'s' if minutes != 1 else ''}"


def client_ip(request: Request) -> str:
    # Render, Vercel and most proxies put the real client first in X-Forwarded-For.
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


analysis_limiter = RateLimiter(settings.rate_limit_requests, settings.rate_limit_window_seconds)


async def limit_analysis(request: Request) -> None:
    analysis_limiter.check(client_ip(request))
