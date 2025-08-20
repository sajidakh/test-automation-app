from backend.python.main import app as the_app
from fastapi import Request
from fastapi.testclient import TestClient


def test_error_envelope_shape():
    @the_app.get("/boom")  # type: ignore
    def boom(request: Request):
        raise RuntimeError("kaboom")

    client = TestClient(the_app, raise_server_exceptions=False)
    r = client.get("/boom", headers={"x-request-id": "xyz"})
    assert r.status_code == 500
    body = r.json()
    assert body.get("ok") is False
    assert body.get("error", {}).get("code") == "internal_error"
    assert body.get("error", {}).get("request_id") == "xyz"

