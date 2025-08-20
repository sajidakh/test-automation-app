from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="FlowForge Python Bridge")

class RunRequest(BaseModel):
    test: str = "smoke"

@app.get("/health")
def health():
    return {"status": "ok", "service": "python-api"}

@app.post("/run")
def run_tests(req: RunRequest):
    return {"received": req.test, "result": "not-implemented"}
