"""
backend/python/tests/test_auth_cors.py — module overview.
Purpose: explain what this module does, key responsibilities, and where it’s called from.
Usage: imported by routers/services; keep functions small and pure when possible.
"""import importlib
import sys

from fastapi.testclient import TestClient


def reload_app():
    if "main" in sys.modules:
        importlib.reload(sys.modules["main"])
    else:
        import backend.python.main as main  # noqa
    from backend.python.main import app
    return app

def test_secure_ping_401_when_no_key(monkeypatch):
    monkeypatch.setenv("PF_API_KEY", "k")   # require a key
    app = reload_app()
    client = TestClient(app)
    r = client.get("/secure-ping")
    assert r.status_code == 401

def test_secure_ping_200_with_key(monkeypatch):
    monkeypatch.setenv("PF_API_KEY", "k")
    app = reload_app()
    client = TestClient(app)
    r = client.get("/secure-ping", headers={"x-api-key": "k"})
    assert r.status_code == 200
    assert r.json()["pong"] is True

def test_cors_allows_configured_origin(monkeypatch):
    monkeypatch.setenv("PF_CORS_ORIGINS", "http://example.com")
    app = reload_app()
    client = TestClient(app)
    r = client.options("/health", headers={
        "origin": "http://example.com",
        "access-control-request-method": "GET",
        "access-control-request-headers": "content-type",
    })
    assert r.status_code in (200, 204)
    assert r.headers.get("access-control-allow-origin") == "http://example.com"


