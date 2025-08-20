# Testing notes (short)

- Unit tests: marked as `not live` (fast, no server)
- Live tests: marked as `live` (starts uvicorn & hits HTTP)

Commands:
- All:    .\backend\python\.venv\Scripts\python.exe -m pytest -q
- Unit:   .\backend\python\.venv\Scripts\python.exe -m pytest -q -m "not live"
- Live:   .\backend\python\.venv\Scripts\python.exe -m pytest -q -m live -vv

Troubleshoot:
- If live tests stall: .\scripts\stop-dev.ps1 then re-run.
- CORS defaults allow 127.0.0.1:5173 and localhost:5173.
  PF_CORS_ORIGINS supports CSV or JSON list overrides.
