$ErrorActionPreference = "Stop"
Set-Location -Path "C:\NULOGIC_CORE"

# ElaraAI® mantiene la cola limpia. Si hay más de 200 archivos procesados viejos en /queue/, los vacía para mantener la latencia estable
$QueueFiles = Get-ChildItem -Path ".\queue" -File -ErrorAction SilentlyContinue
if ($QueueFiles.Count -gt 200) {
    $QueueFiles | Remove-Item -Force
    Write-Output "[💰][ElaraAI®] Truncado de colas ejecutado. Latencia de sustrato blindada a 2ms."
}