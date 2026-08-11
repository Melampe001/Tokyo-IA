$ErrorActionPreference = "Continue"
Set-Location -Path "E:\TOKYOAPPS_UNIVERSE\01_ACTIVE\NULOGIC_CORE"

Write-Host "===========================================================" -ForegroundColor Cyan
Write-Host "   NULOGIC CORE :: AUDITORÍA INTEGRAL Y VALIDACIÓN GLOBAL  " -ForegroundColor Cyan
Write-Host "===========================================================" -ForegroundColor Cyan

$Passed = 0
$Failed = 0

function Report-Check ($title, $condition, $details) {
    if ($condition) {
        Write-Host "  [OK] $title" -ForegroundColor Green
        if ($details) { Write-Host "       ↳ $details" -ForegroundColor Gray }
        $script:Passed++
    } else {
        Write-Host "  [FAIL] $title" -ForegroundColor Red
        if ($details) { Write-Host "       ↳ $details" -ForegroundColor DarkRed }
        $script:Failed++
    }
}

Write-Host "`n[1/5] Auditando estructura de archivos..." -ForegroundColor Yellow
Report-Check "AGENTS_CORE/phase_sync.py" (Test-Path "AGENTS_CORE\phase_sync.py") "Orquestador principal"
Report-Check "AGENTS_CORE/trading_agent.py" (Test-Path "AGENTS_CORE\trading_agent.py") "Agente de Trading"
Report-Check "AGENTS_CORE/content_agent.py" (Test-Path "AGENTS_CORE\content_agent.py") "Agente de Contenido"
Report-Check "AGENTS_CORE/devops_agent.py" (Test-Path "AGENTS_CORE\devops_agent.py") "Agente DevOps"
Report-Check "health_check.ps1" (Test-Path "health_check.ps1") "Script de diagnostico local"
Report-Check "Archivo .env local" (Test-Path ".env") "Variables de entorno locales"
Report-Check "Archivo .env.example" (Test-Path ".env.example") "Plantilla de variables para Git"

Write-Host "`n[2/5] Auditando integración de dotenv en phase_sync.py..." -ForegroundColor Yellow
if (Test-Path "AGENTS_CORE\phase_sync.py") {
    $PhaseCode = Get-Content "AGENTS_CORE\phase_sync.py" -Raw
    $HasDotenvImport = $PhaseCode -match "from dotenv import load_dotenv"
    $HasLoadDotenv = $PhaseCode -match "load_dotenv\(dotenv_path=env_path\)"
    Report-Check "Importación de dotenv en phase_sync.py" $HasDotenvImport "Librería python-dotenv vinculada"
    Report-Check "Carga activa de .env" $HasLoadDotenv "Configuración de ruta asignada correctamente"
}

Write-Host "`n[3/5] Auditando Hook de Seguridad Git Pre-Push..." -ForegroundColor Yellow
$PrePushPath = ".git\hooks\pre-push"
$PrePushExists = Test-Path $PrePushPath
Report-Check "Existencia del Hook pre-push" $PrePushExists "Ubicación: $PrePushPath"
if ($PrePushExists) {
    $HookContent = Get-Content $PrePushPath -Raw
    $HasHealthCall = $HookContent -match "health_check.ps1"
    Report-Check "Invocación a health_check.ps1 en Hook" $HasHealthCall "Ejecución automatizada vinculada"
}

Write-Host "`n[4/5] Auditando soporte de notificaciones a Discord..." -ForegroundColor Yellow
if (Test-Path "health_check.ps1") {
    $HealthCode = Get-Content "health_check.ps1" -Raw
    $HasDiscordLogic = $HealthCode -match "DISCORD_WEBHOOK_URL"
    $HasExitCode = $HealthCode.Contains('exit $Failed') -or $HealthCode -match 'exit\s+\$Failed'
    Report-Check "Módulo de Discord en health_check.ps1" $HasDiscordLogic "Alertas Webhook configuradas"
    Report-Check "Retorno de exit code en health_check.ps1" $HasExitCode "Compatibilidad para bloqueo en CI/CD"
}

Write-Host "`n[5/5] Ejecutando prueba funcional en vivo del motor multiagente..." -ForegroundColor Yellow
$RunOutput = python AGENTS_CORE/phase_sync.py 2>&1
$RunSuccess = ($LASTEXITCODE -eq 0) -and ($RunOutput -match "ALL_AGENTS_SYNCHRONIZED")
Report-Check "Ejecución completa de ciclo 360° (phase_sync.py)" $RunSuccess "Telemetría recibida sin errores"

Write-Host "`n===========================================================" -ForegroundColor Cyan
Write-Host "                RESULTADO FINAL DE LA AUDITORÍA             " -ForegroundColor Cyan
Write-Host "===========================================================" -ForegroundColor Cyan
Write-Host "  Validaciones correctas (OK):  $Passed" -ForegroundColor Green
Write-Host "  Validaciones fallidas (FAIL): $Failed" -ForegroundColor Red

if ($Failed -eq 0) {
    Write-Host "`n  ESTADO GENERAL: TODOS LOS BLOQUES ESTÁN 100% VALIDADOS Y OPERATIVOS 🚀" -ForegroundColor Green
} else {
    Write-Host "`n  ESTADO GENERAL: EXISTEN $Failed ELEMENTO(S) REQUERIDO(S) POR REVISAR ⚠️" -ForegroundColor Red
}
Write-Host "===========================================================`n"