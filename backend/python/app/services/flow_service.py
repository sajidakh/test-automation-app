"""
backend/python/app/services/flow_service.py — module overview.
Purpose: explain what this module does, key responsibilities, and where it’s called from.
Usage: imported by routers/services; keep functions small and pure when possible.
"""from __future__ import annotations

import time
import uuid
from datetime import datetime
from typing import Any

from ..models.flow import Flow, FlowCreate, FlowRunResult, RunRequest

_FLOWS: dict[str, Flow] = {}

def list_flows() -> list[Flow]:
    return list(_FLOWS.values())

def create_flow(inp: FlowCreate) -> Flow:
    fid = str(uuid.uuid4())
    f = Flow(id=fid, name=inp.name, description=inp.description, created_at=datetime.utcnow())
    _FLOWS[fid] = f
    return f

def run_flow(flow_id: str, req: RunRequest | None = None) -> FlowRunResult:
    if flow_id not in _FLOWS:
        raise KeyError(flow_id)
    t0 = time.perf_counter()
    payload: Any = req.payload if req else {}
    time.sleep(0.05)
    dt_ms = int((time.perf_counter() - t0) * 1000)
    return FlowRunResult(
        run_id=str(uuid.uuid4()),
        flow_id=flow_id,
        status="succeeded",
        duration_ms=dt_ms,
        output={"echo": payload or {}, "message": "flow executed"}
    )


