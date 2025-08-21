"""
backend/python/tests/test_logging.py — module overview.
Purpose: explain what this module does, key responsibilities, and where it’s called from.
Usage: imported by routers/services; keep functions small and pure when possible.
"""from backend.python.main import app
from fastapi.testclient import TestClient


def test_json_logs_present(capsys):
    client = TestClient(app)
    _ = client.get("/health")
    err = capsys.readouterr().err
    # We expect our observability to emit start and end lines in JSON
    assert "request_start" in err
    assert "request_end" in err


