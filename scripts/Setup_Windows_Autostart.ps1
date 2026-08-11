# Script de Registro en Programador de Tareas de Windows
$action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-NoProfile -ExecutionPolicy Bypass -File E:\TOKYOAPPS_UNIVERSE\01_ACTIVE\NULOGIC_CORE\Master_Ignition.ps1"
$trigger = New-ScheduledTaskTrigger -AtStartup
Register-ScheduledTask -TaskName "NULOGIC_CORE_AutoBoot" -Action $action -Trigger $trigger -RunLevel Highest -User "SYSTEM" -ErrorAction SilentlyContinue
Write-Host "[✅] Tarea de Auto-Arranque NULOGIC_CORE_AutoBoot configurada." -ForegroundColor Green
