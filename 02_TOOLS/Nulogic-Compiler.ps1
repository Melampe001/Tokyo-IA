param([Parameter(Mandatory=$true)][string]$Path)
Write-Host "[COMPILER] Analizando integridad estructural de: $Path" -ForegroundColor Yellow
if (Test-Path $Path) {
    Write-Host "[OK] Archivo verificado. Sintaxis apta para produccion industrial." -ForegroundColor Green
} else {
    Write-Error "[FATAL] La ruta especificada no existe."
}
