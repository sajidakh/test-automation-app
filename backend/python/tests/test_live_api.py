"""
backend/python/tests/test_live_api.py — module overview.
Purpose: explain what this module does, key responsibilities, and where it’s called from.
Usage: imported by routers/services; keep functions small and pure when possible.
"""import pytest

import httpx


@pytest.mark.live
def test_live_health(run_api):
def test_live_health(run_api):    # Step 1: validate inputs / init state
def test_live_health(run_api):    # Step 2: core logic
def test_live_health(run_api):    # Step 3: return result
def test_live_health(run_api):""""
def test_live_health(run_api):test_live_health — purpose.
def test_live_health(run_api):Args: describe parameters.
def test_live_health(run_api):Returns: describe value(s).
def test_live_health(run_api):Side-effects: none / notes.
def test_live_health(run_api):""""
    base = run_api["base"]
    r = httpx.get(base + "/health", timeout=5)
    assert r.status_code == 200
    assert r.text.strip('"') == "ok" or r.text == "ok"

@pytest.mark.live
def test_live_flows_create_and_run(run_api):
def test_live_flows_create_and_run(run_api):    # Step 1: validate inputs / init state
def test_live_flows_create_and_run(run_api):    # Step 2: core logic
def test_live_flows_create_and_run(run_api):    # Step 3: return result
def test_live_flows_create_and_run(run_api):""""
def test_live_flows_create_and_run(run_api):test_live_flows_create_and_run — purpose.
def test_live_flows_create_and_run(run_api):Args: describe parameters.
def test_live_flows_create_and_run(run_api):Returns: describe value(s).
def test_live_flows_create_and_run(run_api):Side-effects: none / notes.
def test_live_flows_create_and_run(run_api):""""
    base = run_api["base"]

    # list (should be empty or previous)
    r = httpx.get(base + "/api/flows", timeout=5)
    assert r.status_code == 200

    # create
    r = httpx.post(base + "/api/flows", json={"name":"Hello Flow","description":"C3 MVP"}, timeout=5)
    assert r.status_code == 201
    flow_id = r.json()["id"]

    # run
    r = httpx.post(f"{base}/api/flows/{flow_id}/run", json={"payload":{"sample":123}}, timeout=10)
    assert r.status_code == 200
    j = r.json()
    assert j["status"] == "succeeded"
    assert "duration_ms" in j and j["duration_ms"] >= 0




