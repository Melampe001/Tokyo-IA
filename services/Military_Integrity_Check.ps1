$ErrorActionPreference = "Stop"
Set-Location -Path "C:\NULOGIC_CORE"

$FilesToVerify = @("Start_Elara.ps1", "Start_Elara_Background.ps1", "Start_Elara_Omega.ps1", "Bootstrap_Core.ps1")
$DBPath = ".\VAULT\integrity_ledger.db"

$Ledger = @{}
foreach ($File in $FilesToVerify) {
    if (Test-Path ".\$File") {
        # Calcular el ADN matemático del archivo real
        $Hash = (Get-FileHash -Path ".\$File" -Algorithm SHA256).Hash
        $Ledger[$File] = $Hash
    }
}

# Guardar el registro inmutable dentro del VAULT bloqueado por el sistema operativo
$Ledger | ConvertTo-Json | Set-Content -Path $DBPath -Force
Write-Output "[?] ADN de integridad criptográfica SHA-256 actualizado en VAULT."
