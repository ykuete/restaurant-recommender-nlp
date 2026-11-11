"""Rate limiting for the endpoints that cost money (the LLM summary)."""

from __future__ import annotations

import os

from slowapi import Limiter
from starlette.requests import Request

RECOMMEND_LIMIT = os.getenv("RATE_LIMIT", "30/minute")


def client_ip(request: Request) -> str:
    """The visitor's IP. Hosts like Render sit behind a proxy, so prefer the
    first address in X-Forwarded-For over the proxy's own address."""
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


limiter = Limiter(key_func=client_ip)
