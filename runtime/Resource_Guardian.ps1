$ErrorActionPreference = "Stop"
# Monitorear el hilo de PowerShell actual para asegurar cero fugas de recursos
$Process = Get-Process -Id $PID
$MemoryUsage = [Math]::Round($Process.WorkingSet64 / 1MB, 2)
if ($MemoryUsage -gt 500) {
    # Auto-sanación preventiva si el sub-hilo consume demasiada RAM
    [System.GC]::Collect()
}