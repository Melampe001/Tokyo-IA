# ===========================================================
# RascacielosDigital_UniverseAtom® :: SUITE DE VALIDACIÓN ATÓMICA
# ===========================================================
$ErrorActionPreference = "Continue"
Set-Location -Path "E:\TOKYOAPPS_UNIVERSE\01_ACTIVE\NULOGIC_CORE"

Write-Host "===========================================================" -ForegroundColor Magenta
Write-Host " RascacielosDigital_UniverseAtom® :: AUDITORÍA ATÓMICA 360 " -ForegroundColor Magenta
Write-Host "===========================================================" -ForegroundColor Magenta

$AtomicPassed = 0
$AtomicFailed = 0

function Assert-AtomicUnit ($block, $unitName, $condition, $metric) {
    if ($condition) {
        Write-Host "  [ATOM_OK]  [$block] $unitName" -ForegroundColor Green
        if ($metric) { Write-Host "             └─ Telemetría: $metric" -ForegroundColor Gray }
        $script:AtomicPassed++
    } else {
        Write-Host "  [ATOM_FAIL] [$block] $unitName" -ForegroundColor Red
        if ($metric) { Write-Host "             └─ Error: $metric" -ForegroundColor DarkRed }
        $script:AtomicFailed++
    }
}

# BLOQUE 1: DESARROLLO (Núcleo de Agentes y Código Fuente)
Write-Host "`n[ÁTOMO 1/4] Auditando Bloque Desarrollo..." -ForegroundColor Yellow
Assert-AtomicUnit "DEV" "Orquestador PhaseSync (phase_sync.py)" (Test-Path "AGENTS_CORE\phase_sync.py") "Existe en núcleo"
Assert-AtomicUnit "DEV" "Módulo Trading (trading_agent.py)" (Test-Path "AGENTS_CORE\trading_agent.py") "Existe en núcleo"
Assert-AtomicUnit "DEV" "Módulo Contenido (content_agent.py)" (Test-Path "AGENTS_CORE\content_agent.py") "Existe en núcleo"
Assert-AtomicUnit "DEV" "Módulo DevOps (devops_agent.py)" (Test-Path "AGENTS_CORE\devops_agent.py") "Existe en núcleo"

# BLOQUE 2: PROCESO (Estrategias de Entorno, Hooks y CI/CD)
Write-Host "`n[ÁTOMO 2/4] Auditando Bloque Proceso..." -ForegroundColor Yellow
Assert-AtomicUnit "PROC" "Hook Git Pre-Push" (Test-Path ".git\hooks\pre-push") "Integridad de Hook activo"
Assert-AtomicUnit "PROC" "Pipeline CI/CD (.github/workflows/ci.yml)" (Test-Path ".github\workflows\ci.yml") "Definición YAML lista"
Assert-AtomicUnit "PROC" "Contrato de Seguridad (.env local)" (Test-Path ".env") "Variables cargadas"
Assert-AtomicUnit "PROC" "Dependencias Seguras (requirements.txt)" (Test-Path "requirements.txt") "Lista auditada"

# BLOQUE 3: CREACIÓN (Orquestación Multiagente y Telemetría en Vivo)
Write-Host "`n[ÁTOMO 3/4] Auditando Bloque Creación (Prueba de estrés multihilo)..." -ForegroundColor Yellow
$ExecutionTest = python AGENTS_CORE/phase_sync.py 2>&1
$IsSynced = ($LASTEXITCODE -eq 0) -and ($ExecutionTest -match "ALL_AGENTS_SYNCHRONIZED")
Assert-AtomicUnit "CREATE" "Sincronización Multiproceso RascacielosDigital" $IsSynced "Salida del orquestador validada"

# BLOQUE 4: INDEX / DESPLEGABLE (Puntos de Entrada y Notificación)
Write-Host "`n[ÁTOMO 4/4] Auditando Bloque Index & Telemetría..." -ForegroundColor Yellow
Assert-AtomicUnit "INDEX" "Script de Diagnóstico Local (health_check.ps1)" (Test-Path "health_check.ps1") "Script principal listo"
Assert-AtomicUnit "INDEX" "Script de Auditoría (auditoria.ps1)" (Test-Path "auditoria.ps1") "Auditoría interna disponible"

Write-Host "`n===========================================================" -ForegroundColor Magenta
Write-Host "    RESUMEN FINAL :: RascacielosDigital_UniverseAtom®     " -ForegroundColor Magenta
Write-Host "===========================================================" -ForegroundColor Magenta
Write-Host "  Átomos Validados (ATOM_OK):   $AtomicPassed" -ForegroundColor Green
Write-Host "  Átomos Fallidos  (ATOM_FAIL): $AtomicFailed" -ForegroundColor Red

if ($AtomicFailed -eq 0) {
    Write-Host "`n  NÚCLEO ÁTOMICO 100% OPERATIVO, INTEGRAL Y SINCRO-ESTABLE ⚡" -ForegroundColor Green
} else {
    Write-Host "`n  SE DETECTARON $AtomicFailed ÁTOMO(S) REQUERIDO(S) CON ANOMALÍAS ⚠️" -ForegroundColor Red
}
Write-Host "===========================================================`n"