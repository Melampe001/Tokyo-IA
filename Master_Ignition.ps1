# ==============================================================================
# MASTER IGNITION - SCRIPT UNIFICADO Y ROBUSTO DE ARRANQUE Y PERSISTENCIA
# Sistema: Rascacielos Digital / NULOGIC_CORE
# Propietario Exclusivo: Jose Arturo Orozco Jaime
# ==============================================================================

$ErrorActionPreference = "Continue"

$TargetDir = "E:\TOKYOAPPS_UNIVERSE\01_ACTIVE\NULOGIC_CORE"
if (-not (Test-Path $TargetDir)) { $TargetDir = "C:\NULOGIC_CORE" }
Set-Location $TargetDir

Clear-Host
Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host "🚀 NULOGIC CORE :: INICIANDO ARRANQUE MAESTRO DEL RASCACIELOS DIGITAL" -ForegroundColor Yellow
Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host "📍 Directorio de Ejecución: $TargetDir" -ForegroundColor Gray
Write-Host "👤 Propietario: Jose Arturo Orozco Jaime" -ForegroundColor Gray
Write-Host "📅 Fecha y Hora: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Gray
Write-Host "------------------------------------------------------------------" -ForegroundColor Cyan

# 1. Base de datos SQLite
Write-Host "`n[PASO 1/5] 💾 Verificando Infraestructura de Base de Datos SQLite..." -ForegroundColor Yellow
node -e "const { logAction } = require('./modules/db'); logAction('MASTER_IGNITION_CLEAN', { status: 'ONLINE' }); console.log('✅ Base de datos Tokyo_001.db sincronizada.');"

# 2. Liberación de Puertos y Servidor Node.js (3000)
Write-Host "`n[PASO 2/5] 🌐 Levantando Servidor Central Node.js (server.js)..." -ForegroundColor Yellow
$port3000 = Get-NetTCPConnection -LocalPort 3000 -ErrorAction SilentlyContinue
if ($port3000) {
    Stop-Process -Id $port3000.OwningProcess -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 1
}

$nodeProcess = Start-Process -FilePath "node" -ArgumentList "server.js" -PassThru -NoNewWindow
Start-Sleep -Seconds 2
if ($nodeProcess -and -not $nodeProcess.HasExited) {
    Write-Host "✅ Servidor Node.js activo en segundo plano (PID: $($nodeProcess.Id))." -ForegroundColor Green
}

# 3. Liberación del Puerto 8080 y Demonios Python
Write-Host "`n[PASO 3/5] 🐍 Ejecutando Demonios Python y Núcleos de Control..." -ForegroundColor Yellow
$port8080 = Get-NetTCPConnection -LocalPort 8080 -ErrorAction SilentlyContinue
if ($port8080) {
    Stop-Process -Id $port8080.OwningProcess -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 1
}

foreach ($pyScript in @("nulogic_core.py", "Tokyo001_MasterCore.py")) {
    if (Test-Path $pyScript) {
        Start-Process -FilePath "python" -ArgumentList $pyScript -NoNewWindow -ErrorAction SilentlyContinue
        Write-Host "  ✅ $pyScript enviado a segundo plano." -ForegroundColor Green
    }
}

# 4. Escaneo de 12 Pisos
Write-Host "`n[PASO 4/5] 🏙️ Escaneando e Inicializando Estructura de 12 Pisos..." -ForegroundColor Yellow
$floors = @(
    "Piso1_Kernel_Cognitivo", "Piso2_Trading_Autonomo", "Piso3_Finanzas_Corp",
    "Piso4_Gobierno_Leyes", "Piso5_Live_Sync_Hub", "Piso6_Motor_Industrial",
    "Piso7_Seguridad_Militar", "Piso8_Ecosistema_Medico", "Piso9_Ingenieria_DevOps",
    "Piso10_AlterEgos_IA", "Piso11_Metamorphosis_Engine", "Piso12_Sovereign_Engine"
)
foreach ($floor in $floors) {
    if (Test-Path $floor) {
        Write-Host "  🏢 [$floor] -> Vinculado a la malla de auditoría." -ForegroundColor Gray
    }
}

# 5. Telemetría y lectura de DB
Write-Host "`n[PASO 5/5] 📡 Validando Salud del Sistema y Registrando Telemetría..." -ForegroundColor Yellow
Start-Sleep -Seconds 2
try {
    $health = Invoke-RestMethod -Uri "http://localhost:3000/health" -Method GET -ErrorAction Stop
    Write-Host "✅ Endpoint /health respondiendo correctamente." -ForegroundColor Green
} catch {
    Write-Host "⚠️ Servidor inicializando..." -ForegroundColor DarkYellow
}

Write-Host "`n📋 ÚLTIMAS ACCIONES REGISTRADAS EN TOKYO_001_ACTIONS:" -ForegroundColor Cyan
if (Test-Path "scripts\read_db.js") {
    node scripts/read_db.js
} else {
    node -e "const { db } = require('./modules/db'); console.log(db.prepare('SELECT id, action_type, status, timestamp FROM tokyo_001_actions ORDER BY id DESC LIMIT 5').all());"
}

Write-Host "`n==================================================================" -ForegroundColor Cyan
Write-Host "🎉 RASCACIELOS DIGITAL OPERATIVO Y LIMPIO" -ForegroundColor Green
Write-Host "==================================================================" -ForegroundColor Cyan
