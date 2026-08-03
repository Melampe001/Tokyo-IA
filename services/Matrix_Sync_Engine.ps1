$ErrorActionPreference = "Stop"
Set-Location -Path "C:\NULOGIC_CORE"

$UUID_Actual = (Get-CimInstance Win32_ComputerSystemProduct).UUID
$UUID_Autorizado = "aaac82ef-ea8c-4772-94a3-62081a5a42c0"

function Ejecutar-Sincronizacion-Matriz($RutaUSB) {
    if ($UUID_Actual -eq $UUID_Autorizado) {
        Write-Output "[??] MÁQUINA MATRIZ DETECTADA. Iniciando fusión de datos 24/7..."
        
        # Usar Robocopy nativo de Windows (el método más rápido y seguro del sistema de archivos)
        # /XO: Excluye archivos antiguos (solo copia lo más nuevo)
        # /XD: Protege y no toca tus carpetas restringidas como VAULT o secrets locales
        
        # 1. Traer datos nuevos de la USB a la Laptop Matriz
        Robocopy "$RutaUSB\NULOGIC_CORE" "C:\NULOGIC_CORE" /E /XO /XD "VAULT" "secrets" /R:1 /W:1 /NFL /NDL /NJH /NJS | Out-Null
        
        # 2. Respaldar datos nuevos de la Laptop Matriz hacia la USB para futuras salidas
        Robocopy "C:\NULOGIC_CORE" "$RutaUSB\NULOGIC_CORE" /E /XO /XD "VAULT" "secrets" /R:1 /W:1 /NFL /NDL /NJH /NJS | Out-Null
        
        Write-Output "[?] Fusión de ADN completada. Tu laptop y tu USB comparten el mismo estado de tiempo real."
    }
}
