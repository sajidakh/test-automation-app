<#
  File: scripts/scripts/start-dev.ps1
  Purpose: tooling script. Keep commands idempotent and defensive.
  Usage: see scripts\README.md and repo root README for when/how to run.
#>param(
  [int]$ApiPort = 8000,
  [int]$UiPort  = 5173,
  [string]$ApiKey = "k"  # '' if not needed
)

function Kill-Port {
  param([int]$Port)
  $procIds = Get-NetTCPConnection -State Listen -LocalPort $Port -ErrorAction SilentlyContinue |
             Select-Object -ExpandProperty OwningProcess -Unique
  foreach ($procId in $procIds) { try { Stop-Process -Id $procId -Force -ErrorAction Stop } catch {} }
}

$repo = Split-Path -Parent $PSCommandPath | Split-Path -Parent
Set-Location $repo

# free ports
Kill-Port -Port $ApiPort
Kill-Port -Port $UiPort

# strict CORS to UI origin
$env:PORT = "$ApiPort"
$env:PF_CORS_ORIGINS = "http://localhost:$UiPort"

# start backend in a new window
$apiScript = @"
Set-Location "$repo"
`$env:PORT = "$ApiPort"
`$env:PF_CORS_ORIGINS = "http://localhost:$UiPort"
& ".\backend\python\.venv\Scripts\python.exe" .\main.py
"@
$apiTmp = Join-Path $env:TEMP 'pf_run_api.ps1'
Set-Content -Encoding UTF8 -NoNewline -Path $apiTmp -Value $apiScript
$apiProc = Start-Process powershell -PassThru -ArgumentList @('-NoLogo','-NoProfile','-ExecutionPolicy','Bypass','-File',"`"$apiTmp`"")

# write UI env (vite)
$uiDir = Join-Path $repo 'ui'
$envFile = Join-Path $uiDir '.env.local'
$lines = @("VITE_API_URL=http://localhost:$ApiPort")
if($ApiKey){ $lines += "VITE_API_KEY=$ApiKey" }
Set-Content -Encoding UTF8 -Path $envFile -Value ($lines -join "`r`n")

# start UI in a new window (vite)
$uiScript = @"
Set-Location "$uiDir"
npm run dev -- --port $UiPort
"@
$uiTmp = Join-Path $env:TEMP 'pf_run_ui.ps1'
Set-Content -Encoding UTF8 -NoNewline -Path $uiTmp -Value $uiScript
$uiProc = Start-Process powershell -PassThru -ArgumentList @('-NoLogo','-NoProfile','-ExecutionPolicy','Bypass','-File',"`"$uiTmp`"")

"`nBackend PID: $($apiProc.Id)  -> http://localhost:$ApiPort"
"Frontend PID: $($uiProc.Id) -> http://localhost:$UiPort"
"Use scripts\smoke.ps1 to validate."


