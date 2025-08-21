<#
  File: backend/python.bak.2plus/run_api.ps1
  Purpose: tooling script. Keep commands idempotent and defensive.
  Usage: see scripts\README.md and repo root README for when/how to run.
#># backend/python/run_api.ps1
$ErrorActionPreference = 'Stop'

Import-Module "$PSScriptRoot\..\..\scripts\common.psm1" -Force

$ROOT = Get-ProjectRoot $PSScriptRoot
Import-PFEnv $ROOT

$pyDir = Join-Root $ROOT 'backend\python'

Push-Location $pyDir
try {
  $pyExe = Join-Path $pyDir '.venv\Scripts\python.exe'
  if (-not (Test-Path $pyExe)) { $pyExe = 'python' }

  # SAFE variable names (avoid $Host collision)
  $apiHost = $env:PF_API_HOST
  $apiPort = $env:PF_API_PORT
  $appSpec = $env:PF_API_APP

  if (-not $apiHost) { $apiHost = '127.0.0.1' }
  if (-not $apiPort) { $apiPort = '8000' }
  if (-not $appSpec) { $appSpec = 'main:app' }

  Write-Host ('Starting FastAPI on http://{0}:{1} ({2}) from {3} ...' -f $apiHost, $apiPort, $appSpec, $pyDir)
  & $pyExe -m uvicorn $appSpec --host $apiHost --port $apiPort --reload
}
finally {
  Pop-Location
}


