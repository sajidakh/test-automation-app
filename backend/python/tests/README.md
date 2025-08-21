# tests
- Unit: `-m "not live"` (fast; no servers)
- Live: `-m live` (spawns uvicorn once; waits `/health`; tears down)