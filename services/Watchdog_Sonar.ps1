$ErrorActionPreference = "Stop"
Set-Location -Path "C:\NULOGIC_CORE"

function Invoke-SonarPulse {
    $PythonLog = "C:\NULOGIC_CORE\logs\python_runtime.log"
    $MatrixPath = "C:\NULOGIC_CORE\trig_rules\agents_learning_matrix.json"
    
    # El sonar escanea los logs buscando firmas de error de sintaxis en tiempo real
    if (Test-Path $PythonLog) {
        $LastError = Get-Content $PythonLog -Tail 1 -ErrorAction SilentlyContinue
        if ($LastError -match "SyntaxError" -or $LastError -match "NameError") {
            # Emitir tono acústico de emergencia (Frecuencia de sonar agudo)
            [Console]::Beep(3200, 200)
            
            # Registrar el hallazgo de forma autónoma en la matriz de los GGUF
            if (Test-Path $MatrixPath) {
                $Matrix = Get-Content $MatrixPath | ConvertFrom-Json
                $NuevoError = @{
                    "error_signature" = "Falla detectada por Watchdog Sonar: $LastError";
                    "solution" = "Formatear indentación mediante bloques nativos e inyectar dos puntos obligatorios.";
                    "domain" = "logic"
                }
                $Matrix.known_errors += $NuevoError
                $Matrix.last_sync = (Get-Date -Format "yyyy-MM-dd HH:mm:ss.fff")
                $Matrix | ConvertTo-Json -Depth 4 | Set-Content $MatrixPath -Force
            }
        }
    }
}
Invoke-SonarPulse