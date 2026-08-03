$ErrorActionPreference = "Stop"
Set-Location -Path "C:\NULOGIC_CORE"

function Invoke-DataAtRestShield {
    Write-Output "[🛡️][TokyoAI®] Ejecutando blindaje de datos inertes en reposo..."
    $TargetZip = "C:\NULOGIC_CORE\VAULT\repository_dna.secure"
    $FolderToShield = "C:\NULOGIC_CORE\output"
    
    # Si existen reportes o bitácoras en output, se procesan y empaquetan en RAM
    if (Test-Path $FolderToShield) {
        try {
            $Files = Get-ChildItem -Path $FolderToShield -File
            if ($Files.Count -gt 0) {
                # Leer todos los reportes de salida generados por ElaraAI®
                $RawData = Get-Content -Path "$FolderToShield\* " -Raw -ErrorAction SilentlyContinue
                if ($null -ne $RawData) {
                    # Invocar el motor de cifrado simétrico nativo usando la llave física inmutable del VAULT
                    if (Test-Path "C:\NULOGIC_CORE\services\AES_Crypto_Engine.ps1") {
                        . "C:\NULOGIC_CORE\services\AES_Crypto_Engine.ps1"
                        Invoke-AesEncryption -InputText $RawData -OutputPath $TargetZip
                        Write-Output "[✅][CRIPTO] Historial de datos en reposo convertido a binario seguro AES-256."
                    }
                }
            }
        } catch {
            # Mitigación anti-lag inmediata para no entorpecer los 2ms
        }
    }
}
Invoke-DataAtRestShield