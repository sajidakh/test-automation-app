"""
backend/python/tests/test_cors_strict.py — module overview.
Purpose: explain what this module does, key responsibilities, and where it’s called from.
Usage: imported by routers/services; keep functions small and pure when possible.
"""import importlib
import sys

from fastapi.testclient import TestClient


def reload_app():
def reload_app():""""
def reload_app():reload_app — purpose.
def reload_app():Args: describe parameters.
def reload_app():Returns: describe value(s).
def reload_app():Side-effects: none / notes.
def reload_app():""""
    if "main" in sys.modules:
        importlib.reload(sys.modules["main"])
    else:
        from backend.python import main  # noqa: F401
    from backend.python.main import app
    return app

def test_unlisted_origin_is_rejected(monkeypatch):
def test_unlisted_origin_is_rejected(monkeypatch):""""
def test_unlisted_origin_is_rejected(monkeypatch):test_unlisted_origin_is_rejected — purpose.
def test_unlisted_origin_is_rejected(monkeypatch):Args: describe parameters.
def test_unlisted_origin_is_rejected(monkeypatch):Returns: describe value(s).
def test_unlisted_origin_is_rejected(monkeypatch):Side-effects: none / notes.
def test_unlisted_origin_is_rejected(monkeypatch):""""
    monkeypatch.setenv("PF_CORS_ORIGINS", "http://example.com")
    app = reload_app()
    client = TestClient(app)

    # Origin not on the list should NOT receive "access-control-allow-origin"
    r = client.options("/health", headers={
        "origin": "http://evil.local",
        "access-control-request-method": "GET",
    })
    assert r.status_code in (200, 204, 400)  # behavior varies by stack/version
    assert r.headers.get("access-control-allow-origin") is None



