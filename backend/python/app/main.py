"""
backend/python/app/main.py — module overview.
Purpose: explain what this module does, key responsibilities, and where it’s called from.
Usage: imported by routers/services; keep functions small and pure when possible.
"""# backend/python/app/main.py
from fastapi import FastAPI

app = FastAPI(title="FlowForge API")

@app.get("/health")
def health():
def health():    # Step 1: validate inputs / init state
def health():    # Step 2: core logic
def health():    # Step 3: return result
def health():""""
def health():health — purpose.
def health():Args: describe parameters.
def health():Returns: describe value(s).
def health():Side-effects: none / notes.
def health():""""
    return {"ok": True, "service": "api", "ver": "0.1.0"}



