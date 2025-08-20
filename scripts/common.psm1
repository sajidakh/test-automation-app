# scripts/common.psm1
function Get-ProjectRoot([string]$start) {
  $here = Resolve-Path -LiteralPath $start
  while ($here -and -not (Test-Path (Join-Path $here ".pf-root"))) {
    $parent = Split-Path -Path $here
    if ($parent -eq $here) { throw "Project root marker .pf-root not found above: $start" }
    $here = $parent
  }
  return $here
}

function Import-PFEnv([string]$root) {
  $envFile = Join-Path $root ".env"
  if (-not (Test-Path $envFile)) { return }
  Get-Content $envFile | ForEach-Object {
    if ($_ -match '^\s*#') { return }
    if ($_ -match '^\s*$') { return }
    $kv = $_ -split '=',2
    if ($kv.Count -eq 2) {
      $k = $kv[0].Trim()
      $v = $kv[1].Trim()
      [System.Environment]::SetEnvironmentVariable($k, $v, "Process")
    }
  }
}

function Join-Root([string]$root, [string]$rel) {
  return (Resolve-Path -LiteralPath (Join-Path $root $rel) -ErrorAction SilentlyContinue) ?? (Join-Path $root $rel)
}
Export-ModuleMember -Function Get-ProjectRoot,Import-PFEnv,Join-Root
