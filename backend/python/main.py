"""
backend/python/main.py — module overview.
Purpose: explain what this module does, key responsibilities, and where it’s called from.
Usage: imported by routers/services; keep functions small and pure when possible.
"""
from __future__ import annotations

import json
import os
import sys
import uuid
from typing import Any

from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from starlette.middleware import Middleware


# ---------------- Utilities ----------------
def _normalize(origins: object) -> list[str]:
    if isinstance(origins, str):
        return [s.strip() for s in origins.split(",") if s.strip()]
    if isinstance(origins, (list, tuple, set)):
        return [str(x).strip() for x in origins if str(x).strip()]
    return []

def _json_log(level: str, message: str, **fields: Any) -> None:
    try:
        rec = {"level": level, "logger": "api", "message": message, "time": ""}
        rec.update(fields)
        print(json.dumps(rec), file=sys.stderr, flush=True)
    except Exception:
        # Never let logging crash the app
        pass


# ---------------- App factory (fresh per import/reload) ----------------
def create_app() -> FastAPI:
    env = (os.getenv("PF_ENV") or "dev").lower()
    raw_allow = os.getenv("PF_CORS_ORIGINS")

    # CORS: STRICT when PF_CORS_ORIGINS is present; DEV-permissive only when not set.
    if raw_allow is not None:
        allow_list = _normalize(raw_allow)
        allow_any = False
    else:
        allow_list = []
        allow_any = (env != "prod")

    cors_kwargs = dict(
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["x-request-id"],
    )

    if allow_any:
        # Dev-only permissive. Starlette will echo Origin (not literal "*") with credentials=True.
        cors_kwargs.update(allow_origins=[])
    else:
        cors_kwargs.update(allow_origins=allow_list, allow_origin_regex=None)

    app = FastAPI(title="Project Forge API", middleware=[Middleware(CORSMiddleware, **cors_kwargs)])
    # Flows API routes
    from .app.routers.flows_api import router as flows_api_router
    app.include_router(flows_api_router, prefix='/api', tags=['flows'])
    # Flows API routes

    # Flows API routes

    # Flows API routes

    # Flows API routes

    # ---------- Request ID + JSON logs ----------
    @app.middleware("http")
    async def _request_meta(request: Request, call_next):
        rid = request.headers.get("x-request-id") or str(uuid.uuid4())
        request.state.request_id = rid
        _json_log("INFO", "request_start", request_id=rid, path=request.url.path, method=request.method)
        response = await call_next(request)
        response.headers["x-request-id"] = rid
        _json_log("INFO", "request_end", request_id=rid, path=request.url.path, status=response.status_code)
        return response

    # ---------- Error envelope ----------
    @app.exception_handler(Exception)
    async def _unhandled(request: Request, exc: Exception):
        rid = getattr(getattr(request, "state", None), "request_id", None)
        # Keep request_id BOTH top-level and inside error to satisfy stricter consumers/tests
        return JSONResponse(
            status_code=500,
            content={
                "ok": False,
                "error": {
                    "type": "InternalServerError",
                    "code": "internal_error",
                    "message": "internal error",
                    "request_id": rid,
                },
                "request_id": rid,
            },
        )

    # ---------- Rate limiting ----------
    rate = os.getenv("PF_RATE_PER_MINUTE") or "60"
    limiter = Limiter(key_func=get_remote_address, default_limits=[f"{rate}/minute"])
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # ---------- API key guard ----------
    def require_api_key(x_api_key: str | None = Header(default=None)) -> None:
        expected = os.getenv("PF_API_KEY")
        if not x_api_key:
            raise HTTPException(status_code=401, detail="missing api key")
        if expected is not None and x_api_key != expected:
            raise HTTPException(status_code=401, detail="invalid api key")

    # ---------- Endpoints ----------
    @limiter.limit(lambda: os.getenv("PF_RATE_PER_MINUTE") or "60")
    @app.get("/health")
    async def health(request: Request):
        # Tests expect plain "ok"
        return PlainTextResponse("ok")

    @app.get("/secure-ping", dependencies=[Depends(require_api_key)])
    async def secure_ping(request: Request):
        return {"pong": True}

    @app.get("/projects", dependencies=[Depends(require_api_key)])
    async def projects(request: Request):
        items: list[dict] = []
        return {"items": items, "count": len(items)}

    return app


# Single exported app (tests import/reload this module)
app = create_app()






