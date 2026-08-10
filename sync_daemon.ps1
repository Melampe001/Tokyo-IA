# ===========================================================
# RascacielosDigital_UniverseAtom® :: REAL-TIME CLOUD & DRIVE SYNC
# ===========================================================
$ErrorActionPreference = "SilentlyContinue"
$WorkspacePath = "E:\TOKYOAPPS_UNIVERSE\01_ACTIVE\NULOGIC_CORE"

Write-Host "===========================================================" -ForegroundColor Cyan
Write-Host " DAEMON DE SINCRONIZACIÓN EN TIEMPO REAL :: NULOGIC CORE  " -ForegroundColor Cyan
Write-Host "===========================================================" -ForegroundColor Cyan

# Lista de exclusión estricta por seguridad
$ExcludedPatterns = @("\.env$", "\.git\", "__pycache__", "\.log$", "secrets", "\.tmp$")

function Test-IsSecureFile ($filePath) {
    foreach ($pattern in $script:ExcludedPatterns) {
        if ($filePath -match $pattern) { return $false }
    }
    return $true
}

# Inicializar FileSystemWatcher
$Watcher = New-Object System.IO.FileSystemWatcher
$Watcher.Path = $WorkspacePath
$Watcher.IncludeSubdirectories = $true
$Watcher.EnableRaisingEvents = $true
$Watcher.Filter = "*.*"

Write-Host "[OK] Escuchador activo en: $WorkspacePath" -ForegroundColor Green
Write-Host "[SECURITY] Archivos .env y credenciales excluidos automáticamente." -ForegroundColor Yellow
Write-Host "[STATUS] Presiona CTRL+C para detener el Daemon.`n" -ForegroundColor Gray

$Action = {
    $Path = $Event.SourceEventArgs.FullPath
    $ChangeType = $Event.SourceEventArgs.ChangeType
    
    if (Test-IsSecureFile $Path) {
        $TimeStamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        Write-Host "[$TimeStamp] Detectado cambio [$ChangeType]: $Path" -ForegroundColor DarkCyan
        
        # Ejecutar auto-commit y push a la nube con retraso de consolidación
        Start-Sleep -Seconds 3
        Set-Location -Path "E:\TOKYOAPPS_UNIVERSE\01_ACTIVE\NULOGIC_CORE"
        
        $GitStatus = git status --porcelain
        if ($GitStatus) {
            Write-Host "[$TimeStamp] Sincronizando mejoras con la Nube (GitHub)..." -ForegroundColor Yellow
            git add .
            git commit -m "auto-sync(atom): actualización automática en tiempo real [$TimeStamp]"
            git push origin main
            Write-Host "[$TimeStamp] [OK] Sincronización completada exitosamente.`n" -ForegroundColor Green
        }
    }
}

Register-ObjectEvent $Watcher "Changed" -Action $Action | Out-Null
Register-ObjectEvent $Watcher "Created" -Action $Action | Out-Null
Register-ObjectEvent $Watcher "Deleted" -Action $Action | Out-Null

while ($true) { Start-Sleep -Seconds 1 }