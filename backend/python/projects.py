"""
backend/python/projects.py — module overview.
Purpose: explain what this module does, key responsibilities, and where it’s called from.
Usage: imported by routers/services; keep functions small and pure when possible.
"""from __future__ import annotations

_FAKE_PROJECTS: list[dict] = [
    {"id": "p-001", "name": "LaunchPad", "status": "active"},
    {"id": "p-002", "name": "HyperTune", "status": "paused"},
    {"id": "p-003", "name": "Atlas", "status": "active"},
]

def list_projects() -> list[dict]:
    # In the future this can read from a DB; for now it’s deterministic.
    return _FAKE_PROJECTS.copy()

