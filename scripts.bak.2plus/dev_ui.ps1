# scripts/dev_ui.ps1
$ErrorActionPreference = 'Stop'
Import-Module "$PSScriptRoot\common.psm1" -Force

$ROOT   = Get-ProjectRoot $PSScriptRoot
Import-PFEnv $ROOT

$uiDir  = Join-Root $ROOT 'ui'
$rtFile = Join-Path $ROOT '.pf.runtime.json'

function Test-PortFree([int]$port) {
  try {
    $null = Get-NetTCPConnection -LocalPort $port -ErrorAction Stop
    return $false
  } catch {
    return $true
  }
}

$uiHost = if ($env:PF_UI_HOST) { $env:PF_UI_HOST } else { '127.0.0.1' }
$base   = if ($env:PF_UI_PORT) { [int]$env:PF_UI_PORT } else { 5173 }
$port   = $base

if (-not (Test-PortFree $port)) {
  for ($candidate = $base; $candidate -le ($base + 50); $candidate++) {
    if (Test-PortFree $candidate) { $port = $candidate; break }
  }
}

# Write runtime for Electron
$rt = @{ ui = @{ host = $uiHost; port = $port } }
$rt | ConvertTo-Json -Depth 5 | Set-Content -Path $rtFile -Encoding utf8

Push-Location $uiDir
try {
  npm run dev -- --host $uiHost --port $port --strictPort
}
finally {
  Pop-Location
}
