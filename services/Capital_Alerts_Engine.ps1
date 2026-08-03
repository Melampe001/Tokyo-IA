$ErrorActionPreference = "Stop"

function Disparar-Alerta-Exito {
    # 1. Alerta sonora nativa mediante frecuencias de la placa madre (BEEP)
    # Frecuencia: 2000Hz (Agudo de éxito) | Duración: 150 milisegundos
    [Console]::Beep(2000, 150)
    [Console]::Beep(2500, 200)

    # 2. Alerta visual en la terminal de producción
    $Ese = [char]27
    $Gold = "$Ese[38;2;212;175;55m"
    $Reset = "$Ese[0m"
    Write-Host "`n${Gold}[??][ALERTA OMEGA] ¡Operación de Capital Ejecutada con Éxito en Tiempo Real!${Reset}" -ForegroundColor Yellow
}
