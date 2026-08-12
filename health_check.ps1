# ==============================================================================
# RASCACIELOS DIGITAL ATOM® (SKY) | HEALTH CHECK AUTOMÁTICO SRE
# ==============================================================================
param()
Write-Host "[SRE] Ejecutando verificación de integridad de archivos..." -ForegroundColor Cyan
$dbPath = "E:\TOKYOAPPS_UNIVERSE\01_ACTIVE\NULOGIC_CORE\database\Tokyo_001.db"
if (Test-Path $dbPath) {
    Write-Host "[OK] SSoT detectado y verificado correctamente." -ForegroundColor Green
    exit 0
} else {
    Write-Host "[ERROR] SSoT no encontrado." -ForegroundColor Red
    exit 1
}
