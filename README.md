# TestAutomationApp (Skeleton)

Overview:
- Windows Electron + React desktop UI
- Python (Playwright) automation backend via FastAPI bridge
- Clean, modular structure ready for CI/CD

Folders:
- /ui      -> React + Tailwind UI
- /backend -> Node orchestrator + FastAPI bridge
- /tests   -> Python Playwright tests (self-healing ready)
- /config  -> YAML configs, env files
- /scripts -> PowerShell helpers

Post-Build Validation:
1) Open PowerShell at the project root.
2) Run:
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   .\scripts\validate_structure.ps1

Expected: "All required folders are present."
