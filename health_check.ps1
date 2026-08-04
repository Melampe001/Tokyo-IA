# ===========================================================
# NULOGIC CORE :: SYSTEM HEALTH CHECK SCRIPT
# ===========================================================
$ErrorActionPreference = "SilentlyContinue"

Write-Host "`n===========================================================" -ForegroundColor Cyan
Write-Host "       NULOGIC CORE :: DIAGNÓSTICO DE SALUD DEL SISTEMA     " -ForegroundColor Cyan
Write-Host "===========================================================" -ForegroundColor Cyan

$Passed = 0
$Warnings = 0
$Failed = 0

# 1. VERIFICACIÓN DE ESTRUCTURA DE ARCHIVOS CRÍTICOS
Write-Host "`n[1/4] Auditando estructura de archivos..." -ForegroundColor Yellow

$RequiredFiles = @(
    "AGENTS_CORE\phase_sync.py",
    "AGENTS_CORE\trading_agent.py",
    "AGENTS_CORE\content_agent.py",
    "AGENTS_CORE\devops_agent.py",
    ".env.example",
    ".gitignore"
)

foreach ($file in $RequiredFiles) {
    if (Test-Path $file) {
        Write-Host "  [OK] Archivo encontrado: $file" -ForegroundColor Green
        $Passed++
    } else {
        Write-Host "  [FAIL] Archivo no encontrado: $file" -ForegroundColor Red
        $Failed++
    }
}

# 2. VERIFICACIÓN DE CONFIGURACIÓN .ENV
Write-Host "`n[2/4] Auditando configuración de entorno (.env)..." -ForegroundColor Yellow

if (Test-Path ".env") {
    Write-Host "  [OK] Archivo .env local detectado." -ForegroundColor Green
    $Passed++
    
    $EnvContent = Get-Content ".env"
    $KeysToTest = @("OKX_API_KEY", "BITSO_API_KEY", "INSTAGRAM_ACCESS_TOKEN", "TIKTOK_ACCESS_TOKEN", "GITHUB_TOKEN")
    
    foreach ($key in $KeysToTest) {
        $match = $EnvContent | Select-String -Pattern "^$key=(.+)"
        if ($match) {
            $val = $match.Matches.Groups[1].Value.Trim()
            if ($val -like "*your_*_here*" -or $val -eq "") {
                Write-Host "  [WARN] $key presente pero usando valor por defecto o vacío (Modo MOCK activo)." -ForegroundColor Yellow
                $Warnings++
            } else {
                Write-Host "  [OK] $key configurada correctamente." -ForegroundColor Green
                $Passed++
            }
        } else {
            Write-Host "  [WARN] $key no encontrada en el archivo .env." -ForegroundColor Yellow
            $Warnings++
        }
    }
} else {
    Write-Host "  [WARN] Archivo .env no existe. El sistema operará únicamente en modo MOCK." -ForegroundColor Yellow
    $Warnings++
}

# 3. VERIFICACIÓN DEL ENTORNO PYTHON Y DEPENDENCIAS
Write-Host "`n[3/4] Verificando entorno de ejecución Python..." -ForegroundColor Yellow

$pythonVer = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "  [OK] Python activo: $pythonVer" -ForegroundColor Green
    $Passed++
} else {
    Write-Host "  [FAIL] Python no está disponible en el PATH." -ForegroundColor Red
    $Failed++
}

python -c "import dotenv" 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "  [OK] Módulo 'python-dotenv' instalado y funcional." -ForegroundColor Green
    $Passed++
} else {
    Write-Host "  [WARN] Módulo 'python-dotenv' no detectado." -ForegroundColor Yellow
    $Warnings++
}

# 4. PRUEBA DE INTEGRIDAD Y SINCRO DE GIT
Write-Host "`n[4/4] Verificando estado del repositorio Git..." -ForegroundColor Yellow

$gitBranch = git branch --show-current 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "  [OK] Rama Git activa: $gitBranch" -ForegroundColor Green
    $Passed++
    
    $gitStatus = git status --porcelain
    if ([string]::IsNullOrWhiteSpace($gitStatus)) {
        Write-Host "  [OK] Árbol de trabajo limpio (sin cambios pendientes)." -ForegroundColor Green
        $Passed++
    } else {
        Write-Host "  [WARN] Existen cambios locales no confirmados (uncommitted)." -ForegroundColor Yellow
        $Warnings++
    }
} else {
    Write-Host "  [FAIL] Repositorio Git no inicializado o inaccesible." -ForegroundColor Red
    $Failed++
}

# RESUMEN FINAL DE DIAGNÓSTICO
Write-Host "`n===========================================================" -ForegroundColor Cyan
Write-Host "                  RESUMEN DEL HEALTH CHECK                  " -ForegroundColor Cyan
Write-Host "===========================================================" -ForegroundColor Cyan
Write-Host "  Pruebas exitosas (OK):    $Passed" -ForegroundColor Green
Write-Host "  Advertencias (WARN):      $Warnings" -ForegroundColor Yellow
Write-Host "  Fallos críticos (FAIL):   $Failed" -ForegroundColor Red

if ($Failed -eq 0) {
    Write-Host "`n  ESTADO GENERAL: SISTEMA OPERATIVO Y SALUDABLE 🚀" -ForegroundColor Green
} else {
    Write-Host "`n  ESTADO GENERAL: SE REQUIERE ATENCIÓN EN ELEMENTOS CRÍTICOS ⚠️" -ForegroundColor Red
}
Write-Host "===========================================================`n"