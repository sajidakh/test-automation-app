from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field


class FlowCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = None

class Flow(FlowCreate):
    id: str
    created_at: datetime

class RunRequest(BaseModel):
    payload: dict[str, Any] | None = None

class FlowRunResult(BaseModel):
    run_id: str
    flow_id: str
    status: Literal["succeeded", "failed"]
    duration_ms: int
    output: dict[str, Any]
