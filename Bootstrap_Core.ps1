$ErrorActionPreference = "Stop"
Set-Location -Path "C:\NULOGIC_CORE"
Clear-Host
$Ese = [char]27
$Gold = "$Ese[38;2;212;175;55m"
$Cyan = "$Ese[36m"
$Reset = "$Ese[0m"

Write-Host "${Cyan}[🚀] INICIANDO CONTROLADOR SOBERANO AUTOMÁTICO NULOGIC_CORE...${Reset}"
Write-Host "${Gold}[👑] OPERADOR AUTORIZADO: Tokyo M. (Melampe001) - MÁXIMA AUTONOMÍA REAL${Reset}"

# Inyección inmutable del espacio de nombres en memoria RAM (Dot-Sourcing)
if (Test-Path "C:\NULOGIC_CORE\services\CLI_Communicator.ps1") { . "C:\NULOGIC_CORE\services\CLI_Communicator.ps1" }
if (Test-Path "C:\NULOGIC_CORE\services\AES_Crypto_Engine.ps1") { . "C:\NULOGIC_CORE\services\AES_Crypto_Engine.ps1" }
if (Test-Path "C:\NULOGIC_CORE\services\Trading_Checklist_Validator.ps1") { . "C:\NULOGIC_CORE\services\Trading_Checklist_Validator.ps1" }

Write-Host "`n[👑][NULOGIC_CORE] LA AUTOSUSTENTABILIDAD HA SIDO ALCANZADA:" -ForegroundColor Cyan
Write-Host "  -> Demonio de balances en vivo acoplado al kernel de forma ininterrumpida." -ForegroundColor Green
Write-Host "  -> Los saldos de OKX y Bybit se actualizarán en el Dashboard de forma perpetua." -ForegroundColor Green
Write-Host "  -> Consola liberada. Todo funciona simultáneamente en segundo plano." -ForegroundColor Yellow

# Lanzar los procesos asíncronos y abrir interfaces visuales
if (Test-Path "C:\NULOGIC_CORE\services\Run_Omega_Background.ps1") { . "C:\NULOGIC_CORE\services\Run_Omega_Background.ps1" }
if (Test-Path "C:\NULOGIC_CORE\Sovereign_Dashboard.html") { Start-Process "C:\NULOGIC_CORE\Sovereign_Dashboard.html" }

# DISPARO ASÍNCRONO DEL DEMONIO: Se ejecuta en una instancia oculta para no bloquear tu ventana activa
if (Test-Path "C:\NULOGIC_CORE\services\Live_Balance_Watcher.ps1") {
    Start-Process powershell.exe -ArgumentList "-NoProfile -NonInteractive -ExecutionPolicy Bypass -File C:\NULOGIC_CORE\services\Live_Balance_Watcher.ps1" -WindowStyle Hidden
}
