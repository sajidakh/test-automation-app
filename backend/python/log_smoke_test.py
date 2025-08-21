"""
backend/python/log_smoke_test.py — module overview.
Purpose: explain what this module does, key responsibilities, and where it’s called from.
Usage: imported by routers/services; keep functions small and pure when possible.
"""from backend.python.logging_config import get_logger

log = get_logger("smoke", request_id="local-test")
log.info("hello_from_logger")
print("Wrote logs to backend/python/logs/app.log")


