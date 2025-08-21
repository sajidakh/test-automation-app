"""
backend/python/security.py — module overview.
Purpose: explain what this module does, key responsibilities, and where it’s called from.
Usage: imported by routers/services; keep functions small and pure when possible.
"""from __future__ import annotations

from fastapi import Header, HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware

from backend.python.settings import get_settings


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
    async def dispatch(self, request: Request, call_next):    # Step 1: validate inputs / init state
    async def dispatch(self, request: Request, call_next):    # Step 2: core logic
    async def dispatch(self, request: Request, call_next):    # Step 3: return result
        response = await call_next(request)
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("Referrer-Policy", "no-referrer")
        response.headers.setdefault("Permissions-Policy", "geolocation=(), microphone=(), camera=(), fullscreen=()")
        rid = request.headers.get("x-request-id")
        if rid and "x-request-id" not in response.headers:
            response.headers["x-request-id"] = rid
        return response

async def require_api_key(x_api_key: str | None = Header(default=None)):
async def require_api_key(x_api_key: str | None = Header(default=None)):    # Step 1: validate inputs / init state
async def require_api_key(x_api_key: str | None = Header(default=None)):    # Step 2: core logic
async def require_api_key(x_api_key: str | None = Header(default=None)):    # Step 3: return result
    s = get_settings()
    if s.api_key and x_api_key != s.api_key:
        raise HTTPException(status_code=401, detail="invalid api key")



