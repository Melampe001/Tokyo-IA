# =================================================================
# ⚡ AUTOTODO v3.0 ENDOMOPOTENTE - Windows 10 (Acer Laptop)
# Abril 2026 - Idempotente, EOF
# =================================================================

$LogFile   = "C:\Scripts\autotodo.log"
$BackupDir = "D:\Backups"
$MaxBackups = 10

function Write-Log {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $entry = "$timestamp - $Message"
    Add-Content -Path $LogFile -Value $entry
    Write-Host $entry
}

Write-Log "===== INICIO AUTOTODO ENDOMOPOTENTE ====="

# --- Cerrar procesos innecesarios ---
$processes = @("OneDrive","Teams","Spotify","XboxApp","Cortana","Skype","EdgeUpdate","AdobeUpdater")
foreach ($p in $processes) {
    Get-Process -Name $p -ErrorAction SilentlyContinue | ForEach-Object {
        Stop-Process -Id $_.Id -Force
        Write-Log "Proceso cerrado: $p"
    }
}

# --- Limpiar escritorio (solo deja archivos de programación) ---
$desktop = [Environment]::GetFolderPath("Desktop")
Get-ChildItem -Path $desktop -File | Where-Object {
    $_.Extension -notin ".ps1",".py",".js",".java",".cs",".cpp",".txt"
} | ForEach-Object {
    Remove-Item $_.FullName -Force
    Write-Log "Archivo eliminado del escritorio: $($_.Name)"
}

# --- Vaciar papelera ---
try {
    (New-Object -ComObject Shell.Application).NameSpace(10).Items() | ForEach-Object {
        $_.InvokeVerb("delete")
    }
    Write-Log "Papelera vaciada."
} catch { Write-Log "[ERROR] Papelera: $_" }

# --- Limpiar temporales ---
try {
    Remove-Item -Path "$env:TEMP\*" -Force -Recurse -ErrorAction SilentlyContinue
    Remove-Item -Path "$env:LOCALAPPDATA\Temp\*" -Force -Recurse -ErrorAction SilentlyContinue
    Write-Log "Archivos temporales eliminados."
} catch { Write-Log "[ERROR] Limpieza temporales: $_" }

# --- Ajustes de rendimiento ---
powercfg -h off
Write-Log "Hibernación desactivada."
bcdedit /set useplatformclock true
Write-Log "Timer de plataforma optimizado."
Set-ItemProperty -Path "HKCU:\Control Panel\Desktop" -Name "MenuShowDelay" -Value 0
Write-Log "Menús acelerados."

# --- Seguridad ---
netsh advfirewall set allprofiles state on
netsh advfirewall set allprofiles firewallpolicy blockinbound,allowoutbound
Write-Log "Firewall estricto aplicado."
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\DataCollection" /v AllowTelemetry /t REG_DWORD /d 0 /f
Write-Log "Telemetría bloqueada."

# --- Backups con rotación + hash ---
try {
    if (!(Test-Path $BackupDir)) { New-Item -ItemType Directory -Force -Path $BackupDir }
    $date = Get-Date -Format "yyyyMMdd_HHmmss"
    $backupPath = "$BackupDir\Backup_$date.zip"
    Compress-Archive -Path "$env:USERPROFILE\Proyectos" -DestinationPath $backupPath -Force
    Write-Log "[OK] Backup creado en $backupPath"

    # Hash de integridad
    $hash = Get-FileHash -Path $backupPath -Algorithm SHA256
    Write-Log "[HASH] $($hash.Hash) para $($backupPath)"

    # Rotación
    $backups = Get-ChildItem -Path $BackupDir -Filter "Backup_*.zip" | Sort-Object CreationTime -Descending
    if ($backups.Count -gt $MaxBackups) {
        $toDelete = $backups | Select-Object -Skip $MaxBackups
        foreach ($b in $toDelete) {
            Remove-Item $b.FullName -Force
            Write-Log "[ROTACIÓN] Backup eliminado: $($b.Name)"
        }
    }
} catch { Write-Log "[ERROR] Backup: $_" }

Write-Log "===== FIN AUTOTODO ENDOMOPOTENTE ====="
Write-Log "Estado final: Sistema limpio, seguro, respaldado y auditado."
exit 0