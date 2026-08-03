# NULOGIC_CORE - GUARDIAN ANTI-ENTROPIA (PISO 8)
$targetScript = "E:\TOKYOAPPS_UNIVERSE\01_ACTIVE\NULOGIC_CORE\core\idempotent_closure_handler.py"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "      NULOGIC_CORE :: GUARDIAN DE PRODUCCION 24/7/365     " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

while ($true) {
    Write-Host "[INIT] Arrancando motor de ejecuciones inteligentes Python..." -ForegroundColor Green
    
    # Inicia el proceso Python y monitorea su ciclo de vida
    Start-Process -FilePath "python" -ArgumentList $targetScript -Wait -NoNewWindow

    # Si Python finaliza o choca por cualquier razón externa, el bucle lo revive
    Write-Host "[ALERTA] Proceso detenido. Aplicando resiliencia Anti-Stop..." -ForegroundColor Yellow
    Start-Sleep -Seconds 2
}
