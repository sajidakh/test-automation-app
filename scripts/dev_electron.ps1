$ErrorActionPreference = "Stop"
$root   = Split-Path $PSScriptRoot -Parent
$portFile = Join-Path $root ".ff_ui_port"
$uiPort = 5173
if (Test-Path $portFile) { $uiPort = [int](Get-Content -Raw $portFile) }
$uiUrl = "http://127.0.0.1:$uiPort"

Write-Host "Electron: launching against $uiUrl"

# Wait for UI to be ready (max 90s)
$deadline = (Get-Date).AddSeconds(90)
$ready = $false
while ((Get-Date) -lt $deadline) {
  try {
    $r = Invoke-WebRequest -UseBasicParsing -Uri $uiUrl -TimeoutSec 2
    if ($r.StatusCode -ge 200 -and $r.StatusCode -lt 500) { $ready = $true; break }
  } catch { Start-Sleep -Milliseconds 500 }
}
if (-not $ready) { throw "UI at $uiUrl did not become ready within 90 seconds" }

$env:FF_UI_URL = $uiUrl

Push-Location (Join-Path $root "backend\node")
try {
  npm run start:electron
} finally { Pop-Location }
