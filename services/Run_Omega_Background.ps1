$ErrorActionPreference = "Stop"
Set-Location -Path "C:\NULOGIC_CORE"

# Forzar a Windows a ejecutar el script de Python en un proceso de sistema aislado
# Al usar -NoNewWindow, corre en silencio de fondo sin secuestrar el prompt de la consola
if (Test-Path "C:\NULOGIC_CORE\logic\trading_signals.py") {
    Start-Process python -ArgumentList "C:\NULOGIC_CORE\logic\trading_signals.py" -NoNewWindow
}