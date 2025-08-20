from __future__ import annotations

import platform
from datetime import datetime

from fastapi import APIRouter

router = APIRouter(tags=["health"])

STARTED_AT = datetime.utcnow()

@router.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "uptime_sec": (datetime.utcnow() - STARTED_AT).total_seconds(),
        "python": platform.python_version(),
        "platform": platform.platform(),
    }

