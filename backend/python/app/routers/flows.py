"""
backend/python/app/routers/flows.py — module overview.
Purpose: explain what this module does, key responsibilities, and where it’s called from.
Usage: imported by routers/services; keep functions small and pure when possible.
"""from __future__ import annotations

from fastapi import APIRouter, HTTPException

from ..models import Flow, FlowIn
from ..storage import delete_flow, list_flows, save_flow

router = APIRouter(prefix="/flows", tags=["flows"])

@router.get("", response_model=list[Flow])
def get_flows():
    return list_flows()

@router.post("", response_model=Flow, status_code=201)
def create_flow(flow_in: FlowIn):
    return save_flow(flow_in)

@router.delete("/{flow_id}", status_code=204)
def remove_flow(flow_id: str):
    ok = delete_flow(flow_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Flow not found")


