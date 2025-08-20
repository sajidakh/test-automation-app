param([int[]]$Ports = @(8000,5173))

function Kill-Port {
  param([int]$Port)
  $procIds = Get-NetTCPConnection -State Listen -LocalPort $Port -ErrorAction SilentlyContinue |
             Select-Object -ExpandProperty OwningProcess -Unique
  foreach ($procId in $procIds) { try { Stop-Process -Id $procId -Force -ErrorAction Stop } catch {} }
}

foreach($p in $Ports){ Kill-Port -Port $p }
"Stopped listeners on ports: $($Ports -join ', ')"
