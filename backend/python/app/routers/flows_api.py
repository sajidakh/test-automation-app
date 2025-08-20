from __future__ import annotations

from fastapi import APIRouter, HTTPException

from ..models.flow import Flow, FlowCreate, FlowRunResult, RunRequest
from ..services.flow_service import create_flow, list_flows, run_flow

router = APIRouter()

@router.get("/flows", response_model=list[Flow])
def get_flows() -> list[Flow]:
    return list_flows()

@router.post("/flows", response_model=Flow, status_code=201)
def post_flow(body: FlowCreate) -> Flow:
    return create_flow(body)

@router.post("/flows/{flow_id}/run", response_model=FlowRunResult)
def post_run_flow(flow_id: str, body: RunRequest | None = None) -> FlowRunResult:
    try:
        return run_flow(flow_id, body)
    except KeyError:
        raise HTTPException(status_code=404, detail="Flow not found")

