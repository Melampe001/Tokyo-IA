$ErrorActionPreference = "Stop"
Set-Location -Path "C:\NULOGIC_CORE"

# Función inteligente de TokyoAI®: Si un archivo es alterado, se restaura usando el ADN de Git local
function Validar-Y-Sanar-Codigo {
    $GitStatus = git status --porcelain
    if ($GitStatus -match "M  services/") {
        Write-Output "[🚨][TokyoAI®] ALTERACIÓN DE CÓDIGO DETECTADA. Activando restauración por ADN de Git..."
        # Deshacer cambios corruptos y regresar el archivo a su estado inmaculado original
        git checkout -- services/ | Out-Null
        [Console]::Beep(2500, 300)
    }
    
    # Vaciar buffers de la inundación del inbox si superan los límites de la CPU
    $InboxCount = (Get-ChildItem "C:\NULOGIC_CORE\inbox" -Filter "STRESS_*.json" -ErrorAction SilentlyContinue).Count
    if ($InboxCount -gt 100) {
        Get-ChildItem "C:\NULOGIC_CORE\inbox" -Filter "STRESS_*.json" | Remove-Item -Force
        Write-Output "[🧹][TokyoAI®] Inundación de inbox controlada. 0% de lag en el procesador."
    }
}
Validar-Y-Sanar-Codigo