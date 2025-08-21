<#
  File: scripts.bak.2plus/validate_step2.ps1
  Purpose: tooling script. Keep commands idempotent and defensive.
  Usage: see scripts\README.md and repo root README for when/how to run.
#>
Write-Host "Validating Step 2 files..." -ForegroundColor Cyan
$mustExist = @(
  "ui\package.json",
  "ui\index.html",
  "ui\src\main.tsx",
  "ui\tsconfig.json",
  "ui\tailwind.config.js",
  "ui\postcss.config.js",
  "backend\node\package.json",
  "backend\node\tsconfig.json",
  "backend\node\src\main.ts",
  "backend\python\main.py",
  "backend\python\requirements.txt",
  "backend\python\run_api.ps1"
)
$missing = @()
foreach ($rel in $mustExist) {
  $p = Join-Path $PSScriptRoot ("..\\" + $rel)
  if (-not (Test-Path $p)) { $missing += $rel }
}
if ($missing.Count -eq 0) {
  Write-Host "All Step 2 files are present." -ForegroundColor Green
  exit 0
} else {
  Write-Host ("Missing: " + ($missing -join ", ")) -ForegroundColor Red
  exit 1
}


