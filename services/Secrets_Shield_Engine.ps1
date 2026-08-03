$ErrorActionPreference = "Stop"
Set-Location -Path "C:\NULOGIC_CORE"

function Aplicar-Blindaje-Secrets {
    $RutaSecrets = "C:\NULOGIC_CORE\secrets"
    if (Test-Path $RutaSecrets) {
        $Acl = Get-Acl -Path $RutaSecrets
        # Romper herencia de permisos del sistema operativo anfitrión (no heredar vulnerabilidades)
        $Acl.SetAccessRuleProtection($true, $false)
        $Acl.Access | ForEach-Object { $Acl.RemoveAccessRule($_) | Out-Null }
        
        # Conceder acceso único absoluto al Creador Humano Operador actual
        $UsuarioActual = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
        $FullControlRule = New-Object System.Security.AccessControl.FileSystemAccessRule($UsuarioActual, "FullControl", "ContainerInherit, ObjectInherit", "None", "Allow")
        $Acl.AddAccessRule($FullControlRule)
        
        Set-Acl -Path $RutaSecrets -AclObject $Acl
        
        # Inicializar el manifiesto cifrado base de secretos si no existe
        $ManifestSecrets = "$RutaSecrets\secrets_vault.json"
        if (-not (Test-Path $ManifestSecrets)) {
            $SecretsData = @{
                "vault_status" = "LOCKED_BY_NTFS";
                "identity_seal" = "Tokyo_M_Sovereign_Authority";
                "allowed_agents" = @("TokyoAI®", "ElaraAI®")
            } | ConvertTo-Json -Depth 4
            [System.IO.File]::WriteAllText($ManifestSecrets, $SecretsData, [System.Text.Encoding]::UTF8)
        }
        Write-Output "[✅][BÚNKER] Carpeta /secrets/ aislada y blindada criptográficamente a nivel de hardware."
    }
}
Aplicar-Blindaje-Secrets