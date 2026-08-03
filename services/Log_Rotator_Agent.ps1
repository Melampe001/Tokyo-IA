$ErrorActionPreference = "Stop"
Set-Location -Path "C:\NULOGIC_CORE"
$LogFile = ".\logs\system.log"

if (Test-Path $LogFile) {
    $FileSize = (Get-Item $LogFile).Length
    # Si el archivo supera 1MB, TokyoAI® lo comprime en archive para evitar consumo de memoria RAM en lecturas
    if ($FileSize -gt 1MB) {
        $TimeStamp = Get-Date -Format "yyyyMMdd_HHmmss"
        Move-Item -Path $LogFile -Destination ".\archive\system_$TimeStamp.log" -Force
        New-Item -ItemType File -Path $LogFile -Force | Out-Null
        Write-Output "[🧹][TokyoAI®] Rotación de logs completada. Archivo histórico purificado."
    }
}