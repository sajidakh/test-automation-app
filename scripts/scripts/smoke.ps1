<#
  File: scripts/scripts/smoke.ps1
  Purpose: tooling script. Keep commands idempotent and defensive.
  Usage: see scripts\README.md and repo root README for when/how to run.
#>param(
  [int]$ApiPort = 8000,
  [int]$UiPort  = 5173
)

function Should-Be { param($Cond,$Msg) if(-not $Cond){ throw $Msg } }

"`n--- /health"
$r = Invoke-WebRequest "http://localhost:$ApiPort/health" -TimeoutSec 5
Should-Be ($r.StatusCode -in 200,204) "/health not OK"
$r.Content

"`n--- CORS preflight (expect ACAO=http://localhost:$UiPort)"
$ok = @{
  'origin'="http://localhost:$UiPort"
  'access-control-request-method'='GET'
  'access-control-request-headers'='content-type'
}
$p = Invoke-WebRequest -Method OPTIONS "http://localhost:$ApiPort/health" -Headers $ok -TimeoutSec 5
$p.StatusCode
$p.Headers['Access-Control-Allow-Origin'] | Out-String

"`n--- 404 envelope + request-id"
$r404 = Invoke-WebRequest "http://localhost:$ApiPort/does-not-exist" -SkipHttpErrorCheck
$r404.StatusCode
$r404.Content
$r404.Headers['x-request-id']

"`n--- secure-ping"
$r401 = Invoke-WebRequest "http://localhost:$ApiPort/secure-ping" -SkipHttpErrorCheck
$r401.StatusCode
$r200 = Invoke-WebRequest "http://localhost:$ApiPort/secure-ping" -Headers @{ 'x-api-key'='k' }
$r200.StatusCode
$r200.Content


