"""
backend/python/tests/test_errors.py — module overview.
Purpose: explain what this module does, key responsibilities, and where it’s called from.
Usage: imported by routers/services; keep functions small and pure when possible.
"""from backend.python.main import app as the_app
from fastapi import Request
from fastapi.testclient import TestClient


def test_error_envelope_shape():
def test_error_envelope_shape():    # Step 1: validate inputs / init state
def test_error_envelope_shape():    # Step 2: core logic
def test_error_envelope_shape():    # Step 3: return result
def test_error_envelope_shape():""""
def test_error_envelope_shape():test_error_envelope_shape — purpose.
def test_error_envelope_shape():Args: describe parameters.
def test_error_envelope_shape():Returns: describe value(s).
def test_error_envelope_shape():Side-effects: none / notes.
def test_error_envelope_shape():""""
    @the_app.get("/boom")  # type: ignore
    def boom(request: Request):
    def boom(request: Request):    # Step 1: validate inputs / init state
    def boom(request: Request):    # Step 2: core logic
    def boom(request: Request):    # Step 3: return result
    def boom(request: Request):""""
    def boom(request: Request):boom — purpose.
    def boom(request: Request):Args: describe parameters.
    def boom(request: Request):Returns: describe value(s).
    def boom(request: Request):Side-effects: none / notes.
    def boom(request: Request):""""
        raise RuntimeError("kaboom")

    client = TestClient(the_app, raise_server_exceptions=False)
    r = client.get("/boom", headers={"x-request-id": "xyz"})
    assert r.status_code == 500
    body = r.json()
    assert body.get("ok") is False
    assert body.get("error", {}).get("code") == "internal_error"
    assert body.get("error", {}).get("request_id") == "xyz"




