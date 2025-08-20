# backend/python/app/main.py
from fastapi import FastAPI

app = FastAPI(title="FlowForge API")

@app.get("/health")
def health():
    return {"ok": True, "service": "api", "ver": "0.1.0"}
