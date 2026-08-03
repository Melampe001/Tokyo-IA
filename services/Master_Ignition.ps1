# NULOGIC_CORE :: PISO 10 - ORQUESTADOR MAESTRO UNIVERSAL
$engineScript = "E:\TOKYOAPPS_UNIVERSE\01_ACTIVE\NULOGIC_CORE\core\nulogic_master_engine.py"

Clear-Host
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "     NULOGIC CORE :: SKYCRAPER DIGITAL (12 PISOS 24/7)    " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Estado: PRODUCCION CONTINUA Y MAQUILADO DE EFECTIVO 365D " -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Cyan

while ($true) {
    Write-Host "[SYSTEM] Arrancando motor de maquilado en proceso aislado..." -ForegroundColor Yellow
    
    # Inicia el motor en Python y monitorea su salud
    Start-Process -FilePath "python" -ArgumentList $engineScript -Wait -NoNewWindow

    # Si se detecta un cierre no planificado, el Orquestador lo revive en 2 segundos
    Write-Host "[ALERTA] Evento detectado. Aplicando resiliencia Anti-Entropía (Piso 08)..." -ForegroundColor Red
    Start-Sleep -Seconds 2
}
