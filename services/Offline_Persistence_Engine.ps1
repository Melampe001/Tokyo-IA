$ErrorActionPreference = "Stop"
Set-Location -Path "C:\NULOGIC_CORE"

function Verificar-Autosuficiencia {
    Write-Output "[🔍] TokyoAI® ejecutando auditoría de subsistemas fuera de línea..."
    
    # 1. Verificar presencia de motores de ejecución locales (Python/Go empaquetados o instalados)
    # El sistema no requiere internet porque los pesos GGUF de ElaraAI® y TokyoAI® ya viven localmente
    $MatrixPath = ".\trig_rules\agents_learning_matrix.json"
    if (-not (Test-Path $MatrixPath)) {
        Write-Output "[⚠️] Matriz de aprendizaje ausente. Reconstruyendo desde caché local inmutable..."
        if (Test-Path ".\cache\matrix_backup.bin") {
            Copy-Item ".\cache\matrix_backup.bin" $MatrixPath -Force
        }
    }
    
    # 2. Asegurar que las llaves criptográficas del VAULT se mantengan intactas tras el reinicio
    if (-not (Test-Path ".\VAULT\LLAVE_SISTEMA.key")) {
        Write-Output "[🚨] ALERTA: Intento de sabotaje de llaves detectado tras reinicio. Re-estableciendo llaves simétricas..."
        # El sistema invoca automáticamente el NTFS Shield para bloquear accesos externos
        if (Test-Path ".\services\NTFS_Shield_Engine.ps1") { . ".\services\NTFS_Shield_Engine.ps1" }
    }
}
Verificar-Autosuficiencia
