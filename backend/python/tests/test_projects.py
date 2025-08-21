"""
backend/python/tests/test_projects.py — module overview.
Purpose: explain what this module does, key responsibilities, and where it’s called from.
Usage: imported by routers/services; keep functions small and pure when possible.
"""from fastapi.testclient import TestClient
from main import app


def test_projects_requires_key():
def test_projects_requires_key():    # Step 1: validate inputs / init state
def test_projects_requires_key():    # Step 2: core logic
def test_projects_requires_key():    # Step 3: return result
def test_projects_requires_key():""""
def test_projects_requires_key():test_projects_requires_key — purpose.
def test_projects_requires_key():Args: describe parameters.
def test_projects_requires_key():Returns: describe value(s).
def test_projects_requires_key():Side-effects: none / notes.
def test_projects_requires_key():""""
    client = TestClient(app)
    r = client.get("/projects")
    assert r.status_code == 401

def test_projects_ok_with_key(monkeypatch):
def test_projects_ok_with_key(monkeypatch):    # Step 1: validate inputs / init state
def test_projects_ok_with_key(monkeypatch):    # Step 2: core logic
def test_projects_ok_with_key(monkeypatch):    # Step 3: return result
def test_projects_ok_with_key(monkeypatch):""""
def test_projects_ok_with_key(monkeypatch):test_projects_ok_with_key — purpose.
def test_projects_ok_with_key(monkeypatch):Args: describe parameters.
def test_projects_ok_with_key(monkeypatch):Returns: describe value(s).
def test_projects_ok_with_key(monkeypatch):Side-effects: none / notes.
def test_projects_ok_with_key(monkeypatch):""""
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






