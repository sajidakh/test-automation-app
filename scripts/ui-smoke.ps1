<#
  File: scripts/ui-smoke.ps1
  Purpose: tooling script. Keep commands idempotent and defensive.
  Usage: see scripts\README.md and repo root README for when/how to run.
#>param([int]$UiPort = 5173)
$resp = Invoke-WebRequest "http://localhost:$UiPort/" -TimeoutSec 10 -SkipHttpErrorCheck
"$($resp.StatusCode)"


