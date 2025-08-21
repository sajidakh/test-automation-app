<#
  File: scripts/start-dev.ps1
  Purpose: tooling script. Keep commands idempotent and defensive.
  Usage: see scripts\README.md and repo root README for when/how to run.
#>param([int]$ApiPort=8000,[int]$UiPort=5173,[string]$ApiKey="k")

function Kill-Port { param([int]$Port)
  $pids = Get-NetTCPConnection -State Listen -LocalPort $Port -ErrorAction SilentlyContinue |
          Select-Object -ExpandProperty OwningProcess -Unique
  foreach($pid in $pids){ try{ Stop-Process -Id $pid -Force -ErrorAction Stop }catch{} }
}
function Wait-Tcp([int]$Port,[int]$TimeoutSec=30){
  $t0=Get-Date;$dl=(Get-Date).AddSeconds($TimeoutSec)
  while((Get-Date)-lt $dl){ if(Get-NetTCPConnection -State Listen -LocalPort $Port -ErrorAction SilentlyContinue){return ([int]((Get-Date)-$t0).TotalMilliseconds)}; Start-Sleep -Milliseconds 250 }
  return -1
}
function Wait-Health([int]$Port,[int]$TimeoutSec=60){
  $t0=Get-Date;$dl=(Get-Date).AddSeconds($TimeoutSec)
  while((Get-Date)-lt $dl){
    try{ $r=Invoke-WebRequest "http://localhost:$Port/health" -TimeoutSec 3; if($r.StatusCode -in 200,204){ return ([int]((Get-Date)-$t0).TotalMilliseconds)} }catch{}
    Start-Sleep -Milliseconds 500
  }; return -1
}

$repo = Split-Path -Parent $PSCommandPath | Split-Path -Parent
Set-Location $repo

# Free ports
Kill-Port -Port $ApiPort; Kill-Port -Port $UiPort

# START API in a child process; set env INSIDE the child only
$uvicorn = Join-Path $repo 'backend\python\.venv\Scripts\uvicorn.exe'
$apiCmd  = @"
Set-Location "$repo"
`$env:PORT = "$ApiPort"
`$env:PF_CORS_ORIGINS = "http://localhost:$UiPort"
& "$uvicorn" backend.python.main:app --host 127.0.0.1 --port $ApiPort
"@
$apiTmp = Join-Path $env:TEMP 'pf_run_api.ps1'
Set-Content -Encoding UTF8 -NoNewline -Path $apiTmp -Value $apiCmd
$apiProc = Start-Process powershell -PassThru -ArgumentList @('-NoLogo','-NoProfile','-ExecutionPolicy','Bypass','-File',"`"$apiTmp`"")

Write-Host "[start] API starting (PID $($apiProc.Id)) on http://localhost:$ApiPort" -ForegroundColor Cyan

# Wait for readiness
$tcpMs    = Wait-Tcp    -Port $ApiPort -TimeoutSec 30
if($tcpMs -lt 0){ Write-Host "[start] API TCP didn't open in time" -ForegroundColor Yellow; exit 1 }
Write-Host "[start] TCP listening after ${tcpMs}ms"
$healthMs = Wait-Health -Port $ApiPort -TimeoutSec 60
if($healthMs -lt 0){ Write-Host "[start] /health not OK within 60s" -ForegroundColor Yellow; exit 1 }
Write-Host "[start] /health OK after ${healthMs}ms"

# UI env file
$uiDir   = Join-Path $repo 'ui'
New-Item -ItemType Directory -Force $uiDir | Out-Null
$envFile = Join-Path $uiDir '.env.local'
$lines   = @("VITE_API_URL=http://localhost:$ApiPort")
if($ApiKey){ $lines += "VITE_API_KEY=$ApiKey" }
Set-Content -Encoding UTF8 -Path $envFile -Value ($lines -join "`r`n")

# Start Vite in a child window
$uiCmd = @"
Set-Location "$uiDir"
npm run dev -- --port $UiPort
"@
$uiTmp  = Join-Path $env:TEMP 'pf_run_ui.ps1'
Set-Content -Encoding UTF8 -NoNewline -Path $uiTmp -Value $uiCmd
$uiProc = Start-Process powershell -PassThru -ArgumentList @('-NoLogo','-NoProfile','-ExecutionPolicy','Bypass','-File',"`"$uiTmp`"")

Write-Host "`nBackend PID: $($apiProc.Id)  -> http://localhost:$ApiPort"
Write-Host "Frontend PID: $($uiProc.Id) -> http://localhost:$UiPort"
Write-Host "Use scripts\smoke.ps1 to validate."


