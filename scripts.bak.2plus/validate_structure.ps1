<#
  File: scripts.bak.2plus/validate_structure.ps1
  Purpose: tooling script. Keep commands idempotent and defensive.
  Usage: see scripts\README.md and repo root README for when/how to run.
#>
Write-Host "Validating project structure..." -ForegroundColor Cyan
$expected = @("ui","backend","tests","config","scripts")
$missing = @()
foreach ($f in $expected) {
  if (-not (Test-Path (Join-Path $PSScriptRoot ("..\" + $f)))) { $missing += $f }
}
if ($missing.Count -eq 0) {
  Write-Host "All required folders are present." -ForegroundColor Green
  exit 0
} else {
  Write-Host ("Missing folders: " + ($missing -join ", ")) -ForegroundColor Red
  exit 1
}


