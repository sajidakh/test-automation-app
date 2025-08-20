import pytest

import httpx


@pytest.mark.live
def test_live_health(run_api):
    base = run_api["base"]
    r = httpx.get(base + "/health", timeout=5)
    assert r.status_code == 200
    assert r.text.strip('"') == "ok" or r.text == "ok"

@pytest.mark.live
def test_live_flows_create_and_run(run_api):
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

