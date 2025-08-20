from backend.python.logging_config import get_logger

log = get_logger("smoke", request_id="local-test")
log.info("hello_from_logger")
print("Wrote logs to backend/python/logs/app.log")

