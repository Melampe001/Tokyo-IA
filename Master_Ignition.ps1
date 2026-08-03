# SISTEMA: TOKYO OS | MODO: IGNICIÓN TOTAL
Set-Location "E:\TOKYOAPPS_UNIVERSE\01_ACTIVE\NULOGIC_CORE"
Write-Host "[🚀] TOKYO MASTER: Activando Rascacielos Digital..." -ForegroundColor Magenta
# Iniciar Núcleo de Estado
Start-Process python -ArgumentList "core\operational_excellence.py" -WindowStyle Hidden
# Iniciar Dashboard de Salud
Start-Process "Sovereign_Dashboard.html"
# Iniciar Orquestador de Trading
Start-Process python -ArgumentList "core\sovereign_orchestrator.py"
Write-Host "[✅] SINGULARIDAD OPERATIVA ALCANZADA." -ForegroundColor Green
Pause
