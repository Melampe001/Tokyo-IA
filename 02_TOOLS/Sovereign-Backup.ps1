# RASCACIELO DIGITAL - MOTOR DE RESPALDO DE ALTA RENDIMIENTO
param(
    [string]$Source = "E:\TOKYOAPPS_UNIVERSE\01_ACTIVE\NULOGIC_CORE",
    [string]$DestinationBase = "E:\TOKYOAPPS_UNIVERSE\02_BACKUPS\NULOGIC_CORE_SNAPSHOTS",
    [int]$Threads = 16
)

# 1. GENERAR TIMESTAMPT DE SNAPSHOT
$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$TargetFolder = Join-Path -Path $DestinationBase -ChildPath "SNAPSHOT_$Timestamp"

Write-Host "===========================================================" -ForegroundColor Cyan
Write-Host "   RASCACIELO DIGITAL :: SOVEREIGN BACKUP ENGINE" -ForegroundColor Cyan
Write-Host "===========================================================" -ForegroundColor Cyan
Write-Host " Origen  : $Source" -ForegroundColor Gray
Write-Host " Destino : $TargetFolder" -ForegroundColor Gray
Write-Host " Hilos   : $Threads hilos paralelos (Robocopy /MT)" -ForegroundColor Gray
Write-Host "-----------------------------------------------------------" -ForegroundColor Cyan

# 2. DEFINICIÓN DE MATRIZ DE EXCLUSIÓN (Directorios y Archivos Basura/Pesados)
$ExcludeDirs = @(
    "sandbox_env", 
    "__pycache__", 
    ".venv", 
    "venv", 
    "node_modules", 
    ".git", 
    ".idea", 
    ".vscode", 
    "tmp", 
    "temp", 
    "cache"
)

$ExcludeFiles = @(
    "*.pyc", 
    "*.pyo", 
    "*.log", 
    "*.tmp", 
    "thumbs.db", 
    "desktop.ini", 
    "*.lock"
)

# 3. EJECUCIÓN DE ROBOCOPY
Write-Host "
[🚀] Ejecutando respaldo relámpago con exclusión inteligente..." -ForegroundColor Yellow

$RobocopyArgs = @(
    """",
    """",
    "/E",                           # Subdirectorios incluidos
    "/MT:$Threads",                # Multihilo (Default: 16)
    "/R:1",                         # 1 reintento por archivo bloqueado
    "/W:1",                         # 1 segundo de espera entre reintentos
    "/XD", $ExcludeDirs,            # Exclusión de carpetas
    "/XF", $ExcludeFiles,           # Exclusión de extensiones
    "/NJH", "/NJS", "/NDL", "/NC"   # Salida ultra limpia para consola
)

Start-Process -FilePath "robocopy.exe" -ArgumentList $RobocopyArgs -NoNewWindow -Wait

Write-Host "-----------------------------------------------------------" -ForegroundColor Cyan
Write-Host "[✅] SNAPSHOT CREADO EXITOSAMENTE EN:" -ForegroundColor Green
Write-Host "     $TargetFolder" -ForegroundColor White
Write-Host "===========================================================" -ForegroundColor Cyan