"""
backend/python/tests/conftest.py — module overview.
Purpose: explain what this module does, key responsibilities, and where it’s called from.
Usage: imported by routers/services; keep functions small and pure when possible.
"""from __future__ import annotations

import contextlib
import os
import subprocess
import sys
import time
from pathlib import Path

import httpx
import pytest

API_HOST = "127.0.0.1"
API_PORT = int(os.environ.get("PORT", "8000"))
BASE = f"http://{API_HOST}:{API_PORT}"


def _repo_root() -> str:
    # backend/python/tests -> backend -> repo root
    return str(Path(__file__).resolve().parents[3])


def _wait_health(timeout: float) -> bool:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            r = httpx.get(BASE + "/health", timeout=2.0)
            if r.status_code < 300:
                return True
        except Exception:
            pass
        time.sleep(0.2)
    return False


@pytest.fixture(scope="session")
def run_api():
    """Start uvicorn once, wait for /health, yield base URL, then tear down."""
    env = os.environ.copy()
    env["PORT"] = str(API_PORT)
    env.setdefault("PF_CORS_ORIGINS", "http://localhost:5173")

    root = _repo_root()
    cmd = [
    sys.executable, "-m", "uvicorn", "backend.python.main:app",
    "--host", API_HOST, "--port", str(API_PORT),
    "--access-log",
]

    # Ensure the app can import `backend` from repo root
    old_pp = env.get("PYTHONPATH")
    env["PYTHONPATH"] = root if not old_pp else f"{root}{os.pathsep}{old_pp}"
    env["PYTHONUNBUFFERED"] = "1"

    proc = subprocess.Popen(
    cmd,
    cwd=root,
    env=dict(env, PYTHONPATH=str(root), PYTHONUNBUFFERED="1"),
)

    try:
        assert _wait_health(45.0), "API did not become healthy in time"
        yield {"base": BASE}
    finally:
        with contextlib.suppress(Exception):
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except Exception:
                proc.kill()

# --- ensure unit tests never inherit PF_CORS_ORIGINS from the shell ---
import os
import pytest

@pytest.fixture(autouse=True, scope="session")
def clear_pf_cors_origins():
    os.environ.pop("PF_CORS_ORIGINS", None)
    yield
    os.environ.pop("PF_CORS_ORIGINS", None)

