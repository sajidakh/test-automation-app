# scripts
- **start-dev.ps1** : start uvicorn + Vite, write `.env.local`, wait `/health`
- **smoke.ps1**     : /health, CORS preflight, 404 envelope, secure-ping
- **stop-dev.ps1**  : free ports 8000 / 5173
- **quality-gate.ps1** : Ruff → Mypy → Pytest (`-Fix` for Ruff autofix)