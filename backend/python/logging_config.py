from __future__ import annotations

import json
import logging
import os
import sys
from logging.handlers import RotatingFileHandler

LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_PATH = os.path.join(LOG_DIR, "app.log")

class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%S"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        # forward request_id if using LoggerAdapter
        req_id = getattr(record, "request_id", None)
        if req_id is not None:
            payload["request_id"] = req_id
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False)

def get_logger(name: str, request_id: str | None = None) -> logging.Logger:
    # base logger
    base = logging.getLogger(name)

    # only set handlers once
    if not base.handlers:
        base.setLevel(logging.DEBUG)

        # file rotator
        fh = RotatingFileHandler(LOG_PATH, maxBytes=2_000_000, backupCount=5, encoding="utf-8")
        fh.setFormatter(JsonFormatter())
        base.addHandler(fh)

        # stdout (good for dev and container logs)
        sh = logging.StreamHandler(sys.stdout)
        sh.setFormatter(JsonFormatter())
        base.addHandler(sh)

        # be quiet noisy libs if needed
        logging.getLogger("uvicorn.error").setLevel(logging.WARNING)
        logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
        logging.getLogger("httpx").setLevel(logging.INFO)

    if request_id:
        # attach request_id to each record
        return logging.LoggerAdapter(base, {"request_id": request_id})  # type: ignore[return-value]
    return base
