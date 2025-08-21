"""
backend/python/tests/test_settings.py — module overview.
Purpose: explain what this module does, key responsibilities, and where it’s called from.
Usage: imported by routers/services; keep functions small and pure when possible.
"""def test_settings_defaults():
    from importlib import reload

    from backend.python import settings as s
    reload(s)
    assert "http://127.0.0.1:5173" in s.settings.cors_origins

def test_settings_env_override(monkeypatch):
    monkeypatch.setenv("PF_CORS_ORIGINS", "http://x.com,http://y.com")
    from importlib import reload

    from backend.python import settings as s
    reload(s)
    assert s.settings.cors_origins == ["http://x.com", "http://y.com"]


