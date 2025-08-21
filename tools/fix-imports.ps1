<#
  File: tools/fix-imports.ps1
  Purpose: tooling script. Keep commands idempotent and defensive.
  Usage: see scripts\README.md and repo root README for when/how to run.
#>

param()

$repo = "C:\Project Forge\TestAutomationApp"
$py   = Join-Path $repo "backend\python"

$targets = @(
  "main.py","settings.py","security.py","observability.py","logging_config.py"
) | ForEach-Object { Join-Path $py $_ }

foreach ($f in $targets) {
  if (-not (Test-Path $f)) { continue }
  $orig = Get-Content -Raw -Encoding UTF8 $f
  $new  = $orig

  $new  = [regex]::Replace($new, '(?<![.\w])from\s+settings\s+import\s+', 'from backend.python.settings import ')
  $new  = [regex]::Replace($new, '(?<![.\w])import\s+settings(?![\w.])', 'from backend.python import settings')

  $new  = [regex]::Replace($new, '(?<![.\w])from\s+security\s+import\s+', 'from backend.python.security import ')
  $new  = [regex]::Replace($new, '(?<![.\w])import\s+security(?![\w.])', 'from backend.python import security')

  $new  = [regex]::Replace($new, '(?<![.\w])from\s+observability\s+import\s+', 'from backend.python.observability import ')
  $new  = [regex]::Replace($new, '(?<![.\w])import\s+observability(?![\w.])', 'from backend.python import observability')

  $new  = [regex]::Replace($new, '(?<![.\w])from\s+logging_config\s+import\s+', 'from backend.python.logging_config import ')
  $new  = [regex]::Replace($new, '(?<![.\w])import\s+logging_config(?![\w.])', 'from backend.python import logging_config')

  $new  = [regex]::Replace($new, '(?<![.\w])from\s+main\s+import\s+', 'from backend.python.main import ')
  $new  = [regex]::Replace($new, '(?<![.\w])import\s+main(?![\w.])', 'import backend.python.main as main')

  if ($new -ne $orig) {
    Set-Content -Encoding UTF8 -Path $f -Value $new
  }
}
Write-Host "Import fix completed (scoped)."


