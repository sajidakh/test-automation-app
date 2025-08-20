#requires -PSEdition Core
param(
  [switch]$RunUiSmoke,
  [switch]$RunUiE2E
)

# always execute from the repo root
Set-Location "C:\Project Forge\TestAutomationApp"

Write-Host "`n=== DEV CYCLE START ===" -ForegroundColor Cyan

# 1) stop anything already running on known ports
.\scripts\stop-dev.ps1

# 2) start backend + frontend
.\scripts\start-dev.ps1

# 3) small wait for services to be ready
Start-Sleep -Seconds 5

# 4) backend smoke (health, CORS, 404 envelope, secure-ping)
Write-Host "`n--- BACKEND SMOKE ---" -ForegroundColor Yellow
.\scripts\smoke.ps1

# 5) optional UI smoke
if ($RunUiSmoke) {
  Write-Host "`n--- UI SMOKE ---" -ForegroundColor Yellow
  .\scripts\ui-smoke.ps1
}

# 6) optional UI E2E (Playwright)
if ($RunUiE2E) {
  Write-Host "`n--- UI E2E (Playwright) ---" -ForegroundColor Yellow
  Push-Location .\ui
  try {
    $env:UI_URL="http://localhost:5173"
    $env:API_URL="http://localhost:8000"
    npm run test:e2e
  } finally {
    Pop-Location
  }
}

Write-Host "`n=== DEV CYCLE COMPLETE ===" -ForegroundColor Cyan
