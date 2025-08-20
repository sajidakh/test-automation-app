# scripts/dev_electron.ps1
$ErrorActionPreference = 'Stop'
Import-Module "$PSScriptRoot\common.psm1" -Force

$ROOT   = Get-ProjectRoot $PSScriptRoot
Import-PFEnv $ROOT

$nodeDir = Join-Root $ROOT 'backend\node'
$rtFile  = Join-Path $ROOT '.pf.runtime.json'

$uiHost  = if ($env:PF_UI_HOST) { $env:PF_UI_HOST } else { '127.0.0.1' }
$uiPort  = if ($env:PF_UI_PORT) { [int]$env:PF_UI_PORT } else { 5173 }

if (Test-Path $rtFile) {
  try {
    $rt = Get-Content $rtFile -Raw | ConvertFrom-Json
    if ($rt.ui.host) { $uiHost = $rt.ui.host }
    if ($rt.ui.port) { $uiPort = [int]$rt.ui.port }
  } catch {
    Write-Warning "Failed to read $rtFile; falling back to env/defaults."
  }
}

# Build URL using formatter (no variable right before ':')
$url = ('http://{0}:{1}' -f $uiHost, $uiPort)

Push-Location $nodeDir
try {
  npx wait-on $url

  while ($true) {
    Write-Host "[dev:electron] starting Electron against $url"
    $p = Start-Process -FilePath "npm" -ArgumentList "run","start:electron" -NoNewWindow -PassThru -Wait
    $code = $p.ExitCode
    Write-Host "[dev:electron] Electron exited with code $code"

    if ($code -ne 0) { exit $code }
    Start-Sleep -Seconds 1
  }
}
finally {
  Pop-Location
}
