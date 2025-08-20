from backend.python.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_rate_limit_burst_is_allowed():
    for _ in range(5):
        r = client.get("/health")
        assert r.status_code == 200

