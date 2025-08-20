from backend.python.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_request_id_echo():
    r = client.get("/health", headers={"x-request-id": "abc123"})
    assert r.status_code == 200
    assert r.headers.get("x-request-id") == "abc123"

