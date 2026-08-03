$ErrorActionPreference = "Stop"
Set-Location -Path "C:\NULOGIC_CORE"

function Sincronizar-Suits-Al-Mil {
    $QueueCount = (Get-ChildItem ".\queue" -ErrorAction SilentlyContinue).Count
    if ($QueueCount -gt 50) {
        # Auto-Escalar en silencio absoluto sin abrir ventanas molestas
        Start-Process powershell.exe -ArgumentList "-NoProfile -NonInteractive -ExecutionPolicy Bypass -WindowStyle Hidden -File .\services\Agent_Inbox_Router.ps1"
    }
    if (Test-Path ".\services\Log_Monitor_Agent.ps1") { . ".\services\Log_Monitor_Agent.ps1" }
    if (Test-Path ".\services\Anticipation_Engine.ps1") { . ".\services\Anticipation_Engine.ps1" }
    if (Test-Path ".\services\Voice_Inbox_Bridge.ps1") { . ".\services\Voice_Inbox_Bridge.ps1" }
}
Sincronizar-Suits-Al-Mil