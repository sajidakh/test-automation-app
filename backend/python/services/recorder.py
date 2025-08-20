"""
Playwright recorder session manager (MVP): spawns `playwright codegen`.
- Start: playwright codegen --target <lang> -o <file> <url>
- Stop: terminate process by session id.
Scalable: swap to headless event capture later without API changes.
"""
from __future__ import annotations

import subprocess
import sys
from datetime import datetime
from pathlib import Path
from uuid import UUID, uuid4

from fastapi import HTTPException

SESSIONS: dict[UUID, dict] = {}
DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "recordings"
DATA_DIR.mkdir(parents=True, exist_ok=True)

TARGET_EXT = {
    "python": "py",
    "javascript": "js",
    "java": "java",
    "csharp": "cs",
}


def _out_file(target: str) -> Path:
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
    ext = TARGET_EXT.get(target, "txt")
    return DATA_DIR / f"recording_{ts}.{ext}"


def start_session(url: str, target: str = "python") -> dict:
    exe = [sys.executable, "-m", "playwright", "codegen"]  # robust python -m style
    outfile = _out_file(target)
    args = exe + ["--target", target, "-o", str(outfile), url]

    try:
        # new process group so we can kill children cleanly later on Windows
        proc = subprocess.Popen(
            args,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform.startswith("win") else 0,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Playwright not found. Did you run `python -m playwright install`?")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start recorder: {e}")

    session_id = uuid4()
    SESSIONS[session_id] = {
        "pid": proc.pid,
        "process": proc,
        "output_path": str(outfile),
        "status": "running",
        "url": url,
        "target": target,
    }
    return {
        "session_id": str(session_id),
        "pid": proc.pid,
        "output_path": str(outfile),
        "status": "running",
    }


def stop_session(session_id: UUID) -> dict:
    meta = SESSIONS.get(session_id)
    if not meta:
        raise HTTPException(status_code=404, detail="Session not found")

    proc: subprocess.Popen = meta.get("process")  # type: ignore
    if proc and proc.poll() is None:
        try:
            # terminate process group on Windows; otherwise terminate process
            if sys.platform.startswith("win"):
                subprocess.call(["taskkill", "/F", "/T", "/PID", str(proc.pid)])
            else:
                proc.terminate()
        except Exception as e:
            meta["status"] = "error"
            return {"session_id": str(session_id), "status": "error", "message": f"Failed to stop: {e}"}

    meta["status"] = "stopped"
    return {
        "session_id": str(session_id),
        "status": "stopped",
        "output_path": meta.get("output_path"),
    }

