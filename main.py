"""
main.py — module overview.
Usage: imported by routers/services; keep functions small and pure when possible.
"""
import os
import importlib

# Always reload the real module to pick up env changes
m = importlib.import_module("backend.python.main")
importlib.reload(m)

# Rebuild the FastAPI app using the current environment (PF_CORS_ORIGINS, etc.)
m.app = m.create_app()

# Export the app from this shim too
app = m.app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
