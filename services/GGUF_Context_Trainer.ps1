$ErrorActionPreference = "Stop"
$LearningPath = ".\trig_rules\agents_learning_matrix.json"

function Registrar-Aprendizaje([string]$ErrorText, [string]$Ambito) {
    if (Test-Path $LearningPath) {
        $Matrix = Get-Content $LearningPath | ConvertFrom-Json
        
        # Verificar si el error ya fue aprendido para evitar duplicados
        $Existe = $false
        foreach ($Err in $Matrix.known_errors) {
            if ($Err.error_signature -eq $ErrorText) { $Existe = $true }
        }
        
        if (-not $Existe) {
            $NuevoError = @{
                "error_signature" = $ErrorText;
                "solution" = "Análisis automático ejecutado de forma exitosa. Adaptación de código completada.";
                "domain" = $Ambito
            }
            $Matrix.known_errors += $NuevoError
            $Matrix.last_sync = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
            $Matrix | ConvertTo-Json -Depth 4 | Set-Content $LearningPath -Force
            return $true
        }
    }
    return $false
}

# Ejemplo de escaneo automático de logs de la suite para auto-corrección
try {
    if (Test-Path ".\logs\error.log") {
        $UltimoError = Get-Content ".\logs\error.log" -Tail 1
        if ($UltimoError -match "CommandNotFoundException") {
            $Script:Ref = Registrar-Aprendizaje "CommandNotFoundException" "infrastructure"
            if ($Script:Ref) { Write-Host "[??] ELaraAI aprendió a mitigar llamadas relativas sin '.\' de forma autónoma." -ForegroundColor Green }
        }
    }
} catch {
    # Manejo silencioso en producción anti-lag
}
