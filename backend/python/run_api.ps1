# backend/python/run_api.ps1
$ErrorActionPreference = "Stop"
Import-Module "$PSScriptRoot\..\..\scripts\common.psm1" -Force

$ROOT = Get-ProjectRoot $PSScriptRoot
Import-PFEnv $ROOT

$pyDir = Join-Root $ROOT "backend\python"

Push-Location $pyDir
try {
  $pyExe = Join-Path $pyDir ".venv\Scripts\python.exe"
  if (-not (Test-Path $pyExe)) { $pyExe = "python" }

  $apiHost = $env:PF_API_HOST; if (-not $apiHost) { $apiHost = "127.0.0.1" }
  $apiPort = $env:PF_API_PORT; if (-not $apiPort) { $apiPort = "8000" }
  $appSpec = $env:PF_API_APP;  if (-not $appSpec) { $appSpec = "main:app" }

  Write-Host "Starting FastAPI on http://$apiHost`:$apiPort ($appSpec) from $pyDir ..."
  & $pyExe -m uvicorn $appSpec --host $apiHost --port $apiPort --reload
}
finally { Pop-Location }
