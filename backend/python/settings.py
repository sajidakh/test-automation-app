from __future__ import annotations

import json
import os
from typing import List  # kept for legacy imports elsewhere

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Dev default: include BOTH variants so browsers/Playwright/CI all work
DEV_DEFAULT_CORS = ["http://127.0.0.1:5173", "http://localhost:5173"]


def _parse_list(val: str) -> list[str]:
    """
    Parse either a JSON list (e.g. '["http://a","http://b"]')
    or a CSV string (e.g. 'http://a,http://b') into list[str].
    """
    s = (val or "").strip()
    if not s:
        return []
    if s.startswith("["):
        try:
            loaded = json.loads(s)
            if isinstance(loaded, list):
                return [str(x).strip() for x in loaded if str(x).strip()]
        except Exception:
            pass
    return [p.strip() for p in s.split(",") if p.strip()]


class Settings(BaseSettings):
    # Environment / flags
    env: str = Field(default="dev", alias="PF_ENV")
    debug: bool = Field(default=True, alias="PF_DEBUG")

    # API bind
    api_host: str = Field(default="127.0.0.1", alias="PF_API_HOST")
    api_port: int = Field(default=int(os.getenv("PORT", "8000")), alias="PF_API_PORT")

    # Security / UI
    api_key: str | None = Field(default=None, alias="PF_API_KEY")
    ui_host: str = Field(default="127.0.0.1", alias="PF_UI_HOST")
    ui_port: int = Field(default=5173, alias="PF_UI_PORT")

    # Bind the raw string so pydantic doesn't try to JSON-decode list[str]
    cors_origins_raw: str | None = Field(default=None, alias="PF_CORS_ORIGINS")

    # The actual list we use everywhere (not bound to env)
    cors_origins: list[str] = Field(default_factory=lambda: DEV_DEFAULT_CORS.copy())

    secrets_dir: str | None = Field(default=None, alias="PF_SECRETS_DIR")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        extra="ignore",
    )


# Load .env then instantiate settings once
load_dotenv()
settings = Settings()

# Apply final CORS list:
# - If PF_CORS_ORIGINS is set: parse EXACTLY (CSV or JSON list), no dualize
# - Else: ensure both localhost & 127.0.0.1 are present in dev defaults
if settings.cors_origins_raw:
    parsed = _parse_list(settings.cors_origins_raw)
    settings.cors_origins = parsed or DEV_DEFAULT_CORS.copy()
else:
    s = set(settings.cors_origins or [])
    if "http://localhost:5173" in s:
        s.add("http://127.0.0.1:5173")
    if "http://127.0.0.1:5173" in s:
        s.add("http://localhost:5173")
    settings.cors_origins = sorted(s)
