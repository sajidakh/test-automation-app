"""
Simple JSON-file storage for flows (MVP). Patent-friendly: storage-agnostic
abstraction allowing swap to DB or cloud without API changes.
"""
from __future__ import annotations

import json
from pathlib import Path

from .models import Flow, FlowIn

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
FLOWS_DIR = DATA_DIR / "flows"

FLOWS_DIR.mkdir(parents=True, exist_ok=True)


def _flow_path(flow_id) -> Path:
    return FLOWS_DIR / f"{flow_id}.json"


def save_flow(flow_in: FlowIn) -> Flow:
    flow = Flow(**flow_in.model_dump())
    with _flow_path(flow.id).open("w", encoding="utf-8") as f:
        json.dump(flow.model_dump(), f, ensure_ascii=False, indent=2, default=str)
    return flow


def list_flows() -> list[Flow]:
    items: list[Flow] = []
    for p in FLOWS_DIR.glob("*.json"):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            items.append(Flow(**data))
        except Exception:
            # Skip bad files; in real impl, log & quarantine
            continue
    # newest first
    items.sort(key=lambda f: f.created_at, reverse=True)
    return items


def delete_flow(flow_id) -> bool:
    p = _flow_path(flow_id)
    if p.exists():
        p.unlink()
        return True
    return False

