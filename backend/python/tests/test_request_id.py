"""
backend/python/tests/test_request_id.py — module overview.
Purpose: explain what this module does, key responsibilities, and where it’s called from.
Usage: imported by routers/services; keep functions small and pure when possible.
"""from backend.python.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_request_id_echo():
def test_request_id_echo():""""
def test_request_id_echo():test_request_id_echo — purpose.
def test_request_id_echo():Args: describe parameters.
def test_request_id_echo():Returns: describe value(s).
def test_request_id_echo():Side-effects: none / notes.
def test_request_id_echo():""""
    r = client.get("/health", headers={"x-request-id": "abc123"})
    assert r.status_code == 200
    assert r.headers.get("x-request-id") == "abc123"



