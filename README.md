# Test Automation App — Foundation you can ship

**Why:** reliable, documented, testable base for a desktop MVP that can grow into SaaS.  
**What:** FastAPI backend + Vite/React UI, strict CORS, deterministic tests, PowerShell tooling.

## Quickstart
- Start stack:   `.\scripts\start-dev.ps1`
- Smoke check:   `.\scripts\smoke.ps1`
- Stop stack:    `.\scripts\stop-dev.ps1`
- Tests (all):   `.\backend\python\.venv\Scripts\python.exe -m pytest -q`
  - Unit (fast): `-m "not live"`
  - Live (E2E):  `-m live -vv`
- Quality gate:  `.\scripts\quality-gate.ps1` (add `-Fix` for Ruff autofix)

## Architecture (high level)
- **backend/** → Python application code and API
  - **python/** → FastAPI app & tests
  - **python/app/** → domain code:
    - **models/** (Pydantic shapes)
    - **services/** (business logic; pure & unit-test friendly)
    - **routers/** (FastAPI routes; thin controllers)
- **ui/** → Vite/React dev harness (ping buttons to exercise the API)
- **scripts/** → PowerShell automation (start, smoke, stop, quality-gate, etc.)

## Environment
**Backend**
- `PORT` (default 8000)
- `PF_API_KEY` (for secure endpoints)
- `PF_CORS_ORIGINS` (CSV or JSON: `http://127.0.0.1:5173,http://localhost:5173`
  or `["http://127.0.0.1:5173","http://localhost:5173"]`)

**UI**
- `VITE_API_URL` (default `http://localhost:8000`)
- `VITE_API_KEY` (optional)

**Reliability notes**
- Unit tests **auto-clear** `PF_CORS_ORIGINS` via a session fixture.
- Live tests start uvicorn once, wait `/health`, then tear down.

## Developer loop
1) `.\scripts\start-dev.ps1` → uvicorn + Vite, waits for readiness  
2) Unit tests while coding: `-m "not live"`  
3) Live tests before commit: `-m live -vv`  
4) Commit & push (see shortcuts below)

## Git shortcuts
- `gsafe "message"` — stage + commit + push current branch  
- `gstart feat/name` — create & switch to a feature branch (tracks origin)  
- `gfinish` — merge current branch into `main`, push, clean up  