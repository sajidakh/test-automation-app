<#
  File: .pf.env.ps1
  Purpose: tooling script. Keep commands idempotent and defensive.
  Usage: see scripts\README.md and repo root README for when/how to run.
#># ----- Project Forge portable env -----
# UI defaults (launcher may pick another free port at runtime)
$env:PF_UI_HOST  = "127.0.0.1"
$env:PF_UI_PORT  = "5173"

# API
$env:PF_API_HOST = "127.0.0.1"
$env:PF_API_PORT = "8000"
$env:PF_API_APP  = "main:app"

