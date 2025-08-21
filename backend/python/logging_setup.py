"""
backend/python/logging_setup.py — module overview.
Purpose: explain what this module does, key responsibilities, and where it’s called from.
Usage: imported by routers/services; keep functions small and pure when possible.
"""from __future__ import annotations

import json
import logging
import logging.config
import os
from typing import Any

DEFAULT_LEVEL = os.getenv("PF_LOG_LEVEL", "INFO")
LOG_JSON = os.getenv("PF_LOG_JSON", "true").lower() in ("1", "true", "yes")
LOG_DIR = os.getenv("PF_LOG_DIR", "logs")
os.makedirs(LOG_DIR, exist_ok=True)

class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "time": self.formatTime(record, "%Y-%m-%dT%H:%M:%S"),
        }
        # Optional extras (request_id, path, etc.)
        for key in ("request_id", "path", "method", "status"):
            if hasattr(record, key):
                payload[key] = getattr(record, key)
        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False)

def config() -> None:
    fmt = "%(asctime)s %(levelname)s %(name)s - %(message)s"
    file_handler = {
        "class": "logging.handlers.TimedRotatingFileHandler",
        "filename": os.path.join(LOG_DIR, "api.log"),
        "when": "midnight",
        "backupCount": 7,
        "encoding": "utf8",
        "level": DEFAULT_LEVEL,
        "formatter": "json" if LOG_JSON else "plain",
    }
    console_handler = {
        "class": "logging.StreamHandler",
        "level": DEFAULT_LEVEL,
        "formatter": "json" if LOG_JSON else "plain",
    }
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "plain": {"format": fmt},
                "json": {"()": JsonFormatter},
            },
            "handlers": {
                "console": console_handler,
                "file": file_handler,
            },
            "root": {
                "level": DEFAULT_LEVEL,
                "handlers": ["console", "file"],
            },
            "loggers": {
                "uvicorn": {"level": DEFAULT_LEVEL, "handlers": ["console", "file"], "propagate": False},
                "uvicorn.error": {"level": DEFAULT_LEVEL, "handlers": ["console", "file"], "propagate": False},
                "uvicorn.access": {"level": DEFAULT_LEVEL, "handlers": ["console", "file"], "propagate": False},
            },
        }
    )

