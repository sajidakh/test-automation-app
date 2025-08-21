# tests
- Unit: `-m "not live"` (fast; no servers)
- Live: `-m live` (spawns uvicorn once; waits `/health`; tears down)

**Markers already set in `pytest.ini`** to make the split explicit.