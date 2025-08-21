<#
  File: scripts/quality-gate.ps1
  Purpose: tooling script. Keep commands idempotent and defensive.
  Usage: see scripts\README.md and repo root README for when/how to run.
#>param([switch]$Fix)

Set-Location "C:\Project Forge\TestAutomationApp"

$py = ".\backend\python\.venv\Scripts\python.exe"
$ok = $true

# Kill listeners to avoid port races
.\scripts\stop-dev.ps1 | Out-Null

Write-Host "`n== LINT (ruff) ==" -ForegroundColor Cyan
& $py -m ruff --version
$ruffArgs = @('check','backend/python','--config','backend/python/pyproject.toml')
if ($Fix) { $ruffArgs += @('--fix','--unsafe-fixes') }
& $py -m ruff @ruffArgs
if ($LASTEXITCODE -ne 0) { $ok = $false }

Write-Host "`n== TYPES (mypy) ==" -ForegroundColor Cyan
& $py -m mypy -p backend.python --config-file .\mypy.ini
if ($LASTEXITCODE -ne 0) { $ok = $false }

Write-Host "`n== TESTS (pytest) ==" -ForegroundColor Cyan
$env:PORT = "8000"
$env:PF_CORS_ORIGINS = "http://localhost:5173"
& $py -m pytest -q
if ($LASTEXITCODE -ne 0) { $ok = $false }

if ($ok) { Write-Host "`n✅ QUALITY GATE PASSED" -ForegroundColor Green; exit 0 }
else     { Write-Host "`n❌ QUALITY GATE FAILED" -ForegroundColor Red;   exit 1 }


