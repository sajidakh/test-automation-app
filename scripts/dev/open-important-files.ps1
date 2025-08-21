<#
  File: scripts/dev/open-important-files.ps1
  Purpose: tooling script. Keep commands idempotent and defensive.
  Usage: see scripts\README.md and repo root README for when/how to run.
#>

$ErrorActionPreference = 'Stop'
Import-Module "$PSScriptRoot\..\common.psm1" -Force
$ROOT = Get-ProjectRoot $PSScriptRoot
$paths = @(
  'backend\node\tsconfig.json',
  'backend\node\tsconfig.electron.json',
  'backend\node\package.json',
  'backend\node\src\main.ts',
  'backend\node\preload.js',
  'ui\vite.config.ts',
  '.pf.env.ps1'
)
foreach ($rel in $paths) {
  $p = Join-Root $ROOT $rel
  if (Test-Path $p) { Start-Process notepad.exe $p } else { Write-Warning "Missing: $rel" }
}


