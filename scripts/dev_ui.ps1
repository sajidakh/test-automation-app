<#
  File: scripts/dev_ui.ps1
  Purpose: tooling script. Keep commands idempotent and defensive.
  Usage: see scripts\README.md and repo root README for when/how to run.
#>$ErrorActionPreference = "Stop"
$root   = Split-Path $PSScriptRoot -Parent     # -> C:\Project Forge\TestAutomationApp
$uiDir  = Join-Path $root "ui"
$portFile = Join-Path $root ".ff_ui_port"

# Preferred base port (env override supported)
$base = [int]([Environment]::GetEnvironmentVariable("FF_UI_PORT"))
if (-not $base) { $base = 5173 }

function Test-PortFree([int]$p) { -not (Test-NetConnection 127.0.0.1 -Port $p -InformationLevel Quiet) }

$port = $base
while (-not (Test-PortFree $port)) { $port++ }

# Persist the chosen port so Electron reads the same one
$port | Out-File -Encoding ascii -NoNewline $portFile

Push-Location $uiDir
try {
  npm run dev -- --host 127.0.0.1 --port $port --strictPort
} finally { Pop-Location }


