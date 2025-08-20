from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter

from ...services.recorder import start_session, stop_session
from ..models import RecordStartRequest

router = APIRouter(prefix="/record", tags=["record"])

@router.post("/start")
def record_start(req: RecordStartRequest) -> dict:
    return start_session(req.url, req.target)

@router.post("/stop/{session_id}")
def record_stop(session_id: UUID) -> dict:
    return stop_session(session_id)

