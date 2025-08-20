# Thin wrapper to launch the FastAPI dev server via backend/python/run_api.ps1
param(
  [string]$ApiHost,
  [int]   $ApiPort,
  [string]$AppSpec
)

$ErrorActionPreference = "Stop"

$ROOT  = "C:\Project Forge\TestAutomationApp"
$pyRun = Join-Path $ROOT "backend\python\run_api.ps1"
if (!(Test-Path $pyRun)) { throw "Missing $pyRun" }

# surface overrides to the child script via env
if ($PSBoundParameters.ContainsKey("ApiHost")) { $env:PF_API_HOST = $ApiHost }
if ($PSBoundParameters.ContainsKey("ApiPort")) { $env:PF_API_PORT = [string]$ApiPort }
if ($PSBoundParameters.ContainsKey("AppSpec")) { $env:PF_API_APP  = $AppSpec }

# delegate
pwsh -ExecutionPolicy Bypass -File $pyRun
