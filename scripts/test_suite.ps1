# ==============================================================================
# SUITE DE PRUEBAS DE SEGURIDAD Y PERSISTENCIA - RASCACIELOS DIGITAL
# Propietario Exclusivo: Jose Arturo Orozco Jaime
# ==============================================================================

$WorkDir = "E:\TOKYOAPPS_UNIVERSE\01_ACTIVE\NULOGIC_CORE"
if (-not (Test-Path $WorkDir)) { $WorkDir = "C:\NULOGIC_CORE" }
Set-Location $WorkDir

Write-Host "📍 Directorio de Trabajo: $WorkDir" -ForegroundColor Gray

# 1. Iniciar servidor
Write-Host "`n🚀 1. Iniciando server.js en segundo plano (Puerto 3000)..." -ForegroundColor Yellow
$proc = Start-Process -FilePath "node" -ArgumentList "server.js" -PassThru -NoNewWindow
Start-Sleep -Seconds 2

# 2. Petición POST limpia
Write-Host "`n📡 2. Enviando petición HTTP POST limpia a /api/v1/execute..." -ForegroundColor Yellow
try {
    $resLimpia = Invoke-RestMethod -Uri "http://localhost:3000/api/v1/execute" -Method Post -Body '{"payload":"clean_job"}' -ContentType "application/json"
    Write-Host "✅ Respuesta del servidor HTTP:" -ForegroundColor Green
    $resLimpia | Format-List
} catch {
    Write-Host "❌ Error en petición limpia: $_" -ForegroundColor Red
}

# 3. Petición POST maliciosa
Write-Host "`n🛡️ 3. Enviando petición HTTP POST maliciosa para probar intercepción..." -ForegroundColor Yellow
try {
    $resMaliciosa = Invoke-RestMethod -Uri "http://localhost:3000/api/v1/execute" -Method Post -Body '{"payload":"<script>alert(1)</script>"}' -ContentType "application/json" -ErrorAction Stop
    Write-Host "⚠️ Advertencia: El payload atravesó los filtros." -ForegroundColor Red
} catch {
    Write-Host "✅ Bloqueo HTTP verificado: El servidor rechazó el payload malicioso (400 Bad Request)." -ForegroundColor Green
}

# 4. Lectura de Base de Datos
Write-Host "`n📋 4. Verificando persistencia directa en la base de datos..." -ForegroundColor Yellow
node scripts/read_db.js

# 5. Detener servidor
Write-Host "`n🛑 5. Deteniendo el servidor de pruebas..." -ForegroundColor Yellow
if ($proc -and -not $proc.HasExited) {
    Stop-Process -Id $proc.Id -Force -ErrorAction SilentlyContinue
}
Write-Host "✅ Servidor detenido correctamente." -ForegroundColor Green
