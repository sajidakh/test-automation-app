from fastapi.testclient import TestClient
from main import app


def test_projects_requires_key():
    client = TestClient(app)
    r = client.get("/projects")
    assert r.status_code == 401

def test_projects_ok_with_key(monkeypatch):
    monkeypatch.setenv("PF_API_KEY", "k")
    from importlib import reload

    import main as m
    reload(m)
    client = TestClient(m.app)
    r = client.get("/projects", headers={"x-api-key": "k"})
    assert r.status_code == 200
    data = r.json()
    assert "items" in data and isinstance(data["items"], list)
    assert data["count"] == len(data["items"])



