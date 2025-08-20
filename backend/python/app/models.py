"""
Pydantic models for API I/O and internal state.
Directive-aligned: typed, documented, version-friendly, testable.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class FlowIn(BaseModel):
    """Incoming flow payload from UI or other API clients."""
    name: str = Field(min_length=1, max_length=200)
    steps: list[dict[str, Any]] = Field(default_factory=list)  # generic, future-proof


class Flow(FlowIn):
    """Stored flow representation."""
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class RecordStartRequest(BaseModel):
    """Start a codegen recorder session for a URL."""
    url: str
    target: str = Field(default="python", pattern="^(python|javascript|java|csharp)$")


class RecordSession(BaseModel):
    """Recorder session tracking."""
    session_id: UUID
    pid: int | None = None
    output_path: str | None = None
    status: str = "starting"  # starting | running | stopped | error
    message: str | None = None

