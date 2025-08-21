"""
backend/python/tests/test_cors_strict.py — module overview.
Purpose: explain what this module does, key responsibilities, and where it’s called from.
Usage: imported by routers/services; keep functions small and pure when possible.
"""import importlib
import sys

from fastapi.testclient import TestClient


def reload_app():
    if "main" in sys.modules:
        importlib.reload(sys.modules["main"])
    else:
        from backend.python import main  # noqa: F401
    from backend.python.main import app
    return app

def test_unlisted_origin_is_rejected(monkeypatch):
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


