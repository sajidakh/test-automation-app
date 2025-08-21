# scripts/common.psm1
# Shared helpers: root discovery + .env loader + safe path join

$ErrorActionPreference = 'Stop'

function Get-ProjectRoot([string]$startPath) {
  $dir = Resolve-Path $startPath
  while ($true) {
    $marker = Join-Path $dir ".pf-root"
    if (Test-Path $marker) { return $dir }
    $parent = Split-Path $dir -Parent
    if (-not $parent -or $parent -eq $dir) {
      throw "Project root marker .pf-root not found above: $startPath"
    }
    $dir = $parent
  }
}

function Import-PFEnv([string]$root) {
  $dotenv = Join-Path $root ".env"
  if (-not (Test-Path $dotenv)) { return }
  Get-Content $dotenv | ForEach-Object {
    if ($_ -match '^\s*#') { return }
    if ($_ -match '^\s*$') { return }
    if ($_ -match '^\s*([^=]+)\s*=\s*(.*)\s*$') {
      $k = $matches[1].Trim()
      $v = $matches[2]
      
      # strip surrounding quotes if present
      if ($v.StartsWith('"') -and $v.EndsWith('"')) { $v = $v.Substring(1, $v.Length-2) }
      if ($v.StartsWith("'") -and $v.EndsWith("'")) { $v = $v.Substring(1, $v.Length-2) }
      [System.Environment]::SetEnvironmentVariable($k, $v)
    }
  }
}

function Join-Root([string]$root, [string]$rel) {
  # Prefer existing path under root, otherwise fall back to relative from scripts dir
  $candidate = Join-Path $root $rel
  if (Test-Path $candidate -ErrorAction SilentlyContinue) { return $candidate }
  return (Join-Path (Split-Path $PSCommandPath -Parent) $rel)
}

Export-ModuleMember -Function Get-ProjectRoot, Import-PFEnv, Join-Root
