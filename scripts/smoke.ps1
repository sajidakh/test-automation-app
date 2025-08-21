<#
  File: scripts/smoke.ps1
  Purpose: tooling script. Keep commands idempotent and defensive.
  Usage: see scripts\README.md and repo root README for when/how to run.
#>param(
  [int]$ApiPort = 8000,
  [int]$UiPort  = 5173
)

function Print { param($x) if ($null -ne $x) { $x } }

function Wait-Tcp([int]$Port,[int]$TimeoutSec=30){
  $t0=Get-Date; $deadline=(Get-Date).AddSeconds($TimeoutSec)
  while((Get-Date)-lt $deadline){
    if(Get-NetTCPConnection -State Listen -LocalPort $Port -ErrorAction SilentlyContinue){
      return ([int]((Get-Date)-$t0).TotalMilliseconds)
    }
    Start-Sleep -Milliseconds 250
  }
  return -1
}

function Wait-Health([int]$Port,[int]$TimeoutSec=60){
  $t0=Get-Date; $deadline=(Get-Date).AddSeconds($TimeoutSec)
  while((Get-Date)-lt $deadline){
    try{
      # Force IPv4 first (service binds 127.0.0.1); fall back to localhost
      $r = Invoke-WebRequest "http://127.0.0.1:$Port/health" -TimeoutSec 3
      if($r.StatusCode -in 200,204){ return ([int]((Get-Date)-$t0).TotalMilliseconds) }
    } catch {}
    try{
      $r = Invoke-WebRequest "http://localhost:$Port/health" -TimeoutSec 3
      if($r.StatusCode -in 200,204){ return ([int]((Get-Date)-$t0).TotalMilliseconds) }
    } catch {}
    Start-Sleep -Milliseconds 500
  }
  return -1
}

Write-Host "`n[smoke] Checking API on http://localhost:$ApiPort ..." -ForegroundColor Cyan

$tcpMs = Wait-Tcp -Port $ApiPort -TimeoutSec 30
if($tcpMs -lt 0){ Write-Host "[smoke] API TCP listener not up after 30s" -ForegroundColor Yellow; exit 1 }
Write-Host "[smoke] TCP listening after ${tcpMs}ms"

$httpMs = Wait-Health -Port $ApiPort -TimeoutSec 60
if($httpMs -lt 0){ Write-Host "[smoke] /health not OK after 60s" -ForegroundColor Yellow; exit 1 }
Write-Host "[smoke] /health OK after ${httpMs}ms"

"`n--- /health"
$r = Invoke-WebRequest "http://127.0.0.1:$ApiPort/health" -TimeoutSec 5
Print $r.Content

"`n--- CORS preflight (expect ACAO=http://localhost:$UiPort)"
$ok = @{
  'origin'="http://localhost:$UiPort"
  'access-control-request-method'='GET'
  'access-control-request-headers'='content-type'
}
$p = Invoke-WebRequest -Method OPTIONS "http://127.0.0.1:$ApiPort/health" -Headers $ok -TimeoutSec 5
Print ([int]$p.StatusCode)
Print ($p.Headers['Access-Control-Allow-Origin'])

"`n--- 404 envelope + request-id"
$r404 = Invoke-WebRequest "http://127.0.0.1:$ApiPort/does-not-exist" -SkipHttpErrorCheck
Print ([int]$r404.StatusCode)
Print $r404.Content
Print $r404.Headers['x-request-id']

"`n--- secure-ping"
$r401 = Invoke-WebRequest "http://127.0.0.1:$ApiPort/secure-ping" -SkipHttpErrorCheck
Print ([int]$r401.StatusCode)
$r200 = Invoke-WebRequest "http://127.0.0.1:$ApiPort/secure-ping" -Headers @{ 'x-api-key'='k' }
Print ([int]$r200.StatusCode)
Print $r200.Content

