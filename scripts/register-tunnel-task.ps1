Param(
  [string]$ProjectRoot = "C:\\dev\\spectra",
  [string]$TaskName = "SPECTRA Tunnel",
  [string]$UserId = "S-1-5-18",
  [string]$CloudflaredPath = "C:\\dev\\bin\\cloudflared.exe",
  [string]$ConfigPath = "C:\\ProgramData\\cloudflared\\config.yml",
  [string]$TunnelName = "spectra"
)

if (-not (Test-Path $CloudflaredPath)) {
  Write-Error "cloudflared.exe not found: $CloudflaredPath"
  exit 1
}

if (-not (Test-Path $ConfigPath)) {
  Write-Error "config.yml not found: $ConfigPath"
  exit 1
}

$action = New-ScheduledTaskAction `
  -Execute $CloudflaredPath `
  -Argument "tunnel --config `"$ConfigPath`" run $TunnelName" `
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
  -Description "SPECTRA Cloudflare Tunnel" `
  -Force

Write-Host "Registered scheduled task: $TaskName"
