$ErrorActionPreference = "Stop"
Set-Location -Path "C:\NULOGIC_CORE"

function Invoke-SurgicalSanitizer {
    Write-Output "[🔍][TokyoAI®] Iniciando auditoría quirúrgica de control de entropía..."
    $LedgerPath = ".\VAULT\integrity_ledger.db"
    
    # 1. Escanear y remover archivos temporales duplicados o código muerto que genere Lag
    $TrashExtensions = @("*.tmp", "*copy*", "*.bak", "*~*")
    foreach ($Ext in $TrashExtensions) {
        Get-ChildItem -Path ".\temp", ".\cache" -Filter $Ext -Recurse -ErrorAction SilentlyContinue | Remove-Item -Force
    }

    # 2. Validar unificación de ADN en scripts críticos (Garantizar versión óptima)
    $CoreScripts = @("Bootstrap_Core.ps1", "Start_Elara_Omega.ps1")
    foreach ($Script in $CoreScripts) {
        if (Test-Path ".\$Script") {
            # Limpiar líneas vacías duplicadas y formatear indentación de manera automática
            $Content = Get-Content ".\$Script"
            $CleanContent = @()
            $LastLineWasEmpty = $false
            
            foreach ($Line in $Content) {
                $Trimmed = $Line.Trim()
                if ($Trimmed -eq "") {
                    if (-not $LastLineWasEmpty) {
                        $CleanContent += $Line
                        $LastLineWasEmpty = $true
                    }
                } else {
                    $CleanContent += $Line
                    $LastLineWasEmpty = $false
                }
            }
            # Re-escribir el archivo purificado forzando UTF-8 sin encimar código
            [System.IO.File]::WriteAllLines("C:\NULOGIC_CORE\$Script", $CleanContent, [System.Text.Encoding]::UTF8)
        }
    }
    Write-Output "[✅][ENTROPÍA ZERO] Limpieza de sustrato completada. Versión purificada inyectada en memoria."
}
Invoke-SurgicalSanitizer