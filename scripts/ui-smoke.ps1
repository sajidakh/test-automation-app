param([int]$UiPort = 5173)
$resp = Invoke-WebRequest "http://localhost:$UiPort/" -TimeoutSec 10 -SkipHttpErrorCheck
"$($resp.StatusCode)"
