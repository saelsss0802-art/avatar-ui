Param(
  [string]$ProjectRoot = "C:\\dev\\spectra",
  [string]$TaskName = "SPECTRA Core",
  [string]$UserId = "S-1-5-18"
)

$pythonPath = Join-Path $ProjectRoot ".venv\\Scripts\\python.exe"
if (-not (Test-Path $pythonPath)) {
  Write-Error "python.exe not found: $pythonPath"
  exit 1
}

$action = New-ScheduledTaskAction `
  -Execute $pythonPath `
  -Argument "-m uvicorn core.main:app --host 127.0.0.1 --port 8000" `
  -WorkingDirectory $ProjectRoot

$trigger = New-ScheduledTaskTrigger -AtStartup

$settings = New-ScheduledTaskSettingsSet `
  -RestartCount 3 `
  -RestartInterval (New-TimeSpan -Minutes 1) `
  -MultipleInstances IgnoreNew `
  -StartWhenAvailable `
  -ExecutionTimeLimit (New-TimeSpan -Seconds 0) `
  -AllowStartIfOnBatteries `
  -DontStopIfGoingOnBatteries

$principal = New-ScheduledTaskPrincipal `
  -UserId $UserId `
  -LogonType ServiceAccount `
  -RunLevel Highest

Register-ScheduledTask `
  -TaskName $TaskName `
  -Action $action `
  -Trigger $trigger `
  -Settings $settings `
  -Principal $principal `
  -Description "SPECTRA Core (uvicorn)" `
  -Force

Write-Host "Registered scheduled task: $TaskName"
