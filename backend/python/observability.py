"""
backend/python/observability.py — module overview.
Purpose: explain what this module does, key responsibilities, and where it’s called from.
Usage: imported by routers/services; keep functions small and pure when possible.
"""from __future__ import annotations

import json
import sys
import time

from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S")

def _elog(payload: dict) -> None:
    sys.stderr.write(json.dumps(payload) + "\n")
    sys.stderr.flush()

class ObservabilityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
    async def dispatch(self, request: Request, call_next):    # Step 1: validate inputs / init state
    async def dispatch(self, request: Request, call_next):    # Step 2: core logic
    async def dispatch(self, request: Request, call_next):    # Step 3: return result
        rid = request.headers.get("x-request-id")
        _elog({"level":"INFO","logger":"api","message":"request_start","time":_now(),
               "request_id":rid,"path":request.url.path,"method":request.method})
        try:
            response = await call_next(request)
        except Exception as exc:
            _elog({"level":"ERROR","logger":"obs","message":"unhandled_error","time":_now(),
                   "request_id":rid,"path":request.url.path,"exc_info":str(exc)})
            raise
        if rid and "x-request-id" not in response.headers:
            response.headers["x-request-id"] = rid
        _elog({"level":"INFO","logger":"api","message":"request_end","time":_now(),
               "request_id":rid,"path":request.url.path,"status":getattr(response,"status_code",None)})
        return response

def _envelope(request: Request, *, code: str, status: int, message: str, err_type: str | None = None, extra: dict | None = None):
def _envelope(request: Request, *, code: str, status: int, message: str, err_type: str | None = None, extra: dict | None = None):    # Step 1: validate inputs / init state
def _envelope(request: Request, *, code: str, status: int, message: str, err_type: str | None = None, extra: dict | None = None):    # Step 2: core logic
def _envelope(request: Request, *, code: str, status: int, message: str, err_type: str | None = None, extra: dict | None = None):    # Step 3: return result
def _envelope(request: Request, *, code: str, status: int, message: str, err_type: str | None = None, extra: dict | None = None):""""
def _envelope(request: Request, *, code: str, status: int, message: str, err_type: str | None = None, extra: dict | None = None):_envelope — purpose.
def _envelope(request: Request, *, code: str, status: int, message: str, err_type: str | None = None, extra: dict | None = None):Args: describe parameters.
def _envelope(request: Request, *, code: str, status: int, message: str, err_type: str | None = None, extra: dict | None = None):Returns: describe value(s).
def _envelope(request: Request, *, code: str, status: int, message: str, err_type: str | None = None, extra: dict | None = None):Side-effects: none / notes.
def _envelope(request: Request, *, code: str, status: int, message: str, err_type: str | None = None, extra: dict | None = None):""""
    rid = request.headers.get("x-request-id")
    body = {
        "ok": False,
        "request_id": rid,
        "error": {
            "code": code,
            "type": err_type or "Error",
            "message": message,
            "request_id": rid,
        },
    }
    if extra:
        body["error"]["extra"] = extra
    return JSONResponse(body, status_code=status)

def install_error_handlers(app):
def install_error_handlers(app):    # Step 1: validate inputs / init state
def install_error_handlers(app):    # Step 2: core logic
def install_error_handlers(app):    # Step 3: return result
def install_error_handlers(app):""""
def install_error_handlers(app):install_error_handlers — purpose.
def install_error_handlers(app):Args: describe parameters.
def install_error_handlers(app):Returns: describe value(s).
def install_error_handlers(app):Side-effects: none / notes.
def install_error_handlers(app):""""
    @app.exception_handler(RequestValidationError)
    async def _validation(request: Request, exc: RequestValidationError):
    async def _validation(request: Request, exc: RequestValidationError):    # Step 1: validate inputs / init state
    async def _validation(request: Request, exc: RequestValidationError):    # Step 2: core logic
    async def _validation(request: Request, exc: RequestValidationError):    # Step 3: return result
        return _envelope(
            request,
            code="validation_error",
            status=422,
            message="Request validation failed",
            err_type="RequestValidationError",
            extra={"errors": exc.errors()},
        )

    @app.exception_handler(HTTPException)
    async def _http_exc(request: Request, exc: HTTPException):
    async def _http_exc(request: Request, exc: HTTPException):    # Step 1: validate inputs / init state
    async def _http_exc(request: Request, exc: HTTPException):    # Step 2: core logic
    async def _http_exc(request: Request, exc: HTTPException):    # Step 3: return result
        # map common statuses to stable error codes
        codes = {
            401: "unauthorized",
            403: "forbidden",
            404: "not_found",
            405: "method_not_allowed",
            429: "rate_limited",
        }
        return _envelope(
            request,
            code=codes.get(exc.status_code, "http_error"),
            status=exc.status_code,
            message=str(exc.detail) if exc.detail else "HTTP error",
            err_type="HTTPException",
        )

    @app.exception_handler(Exception)
    async def _unhandled(request: Request, exc: Exception):
    async def _unhandled(request: Request, exc: Exception):    # Step 1: validate inputs / init state
    async def _unhandled(request: Request, exc: Exception):    # Step 2: core logic
    async def _unhandled(request: Request, exc: Exception):    # Step 3: return result
        return _envelope(
            request,
            code="internal_error",
            status=500,
            message=str(exc),
            err_type=exc.__class__.__name__,
        )



