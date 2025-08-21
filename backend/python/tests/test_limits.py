"""
backend/python/tests/test_limits.py — module overview.
Purpose: explain what this module does, key responsibilities, and where it’s called from.
Usage: imported by routers/services; keep functions small and pure when possible.
"""from backend.python.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_rate_limit_burst_is_allowed():
    for _ in range(5):
        r = client.get("/health")
        assert r.status_code == 200


