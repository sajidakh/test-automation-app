function gsafe {
  param([Parameter(Mandatory=$true)][string]$Message)
  git add -A
  git commit -m $Message --no-verify
  if ($LASTEXITCODE -ne 0) { return }
  git push
}

function gstart {
  param([Parameter(Mandatory=$true)][string]$Name)
  git fetch origin
  git checkout -b $Name
  git push -u origin $Name
}

function gfinish {
  # merge current branch into main, push, and delete remote branch
  $curr = (git branch --show-current).Trim()
  if ($curr -eq "main") { Write-Host "Already on main." -ForegroundColor Yellow; return }
  git checkout main
  git pull --ff-only
  git merge --no-ff $curr -m "merge $curr"
  if ($LASTEXITCODE -ne 0) { return }
  git push
  git branch -d $curr
  git push origin --delete $curr 2>$null
}