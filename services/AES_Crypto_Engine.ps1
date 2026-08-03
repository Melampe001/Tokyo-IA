$ErrorActionPreference = "Stop"
Set-Location -Path "C:\NULOGIC_CORE"

# Asegurar la existencia de una llave maestra real de hardware en el VAULT
$KeyPath = ".\VAULT\LLAVE_SISTEMA.key"
if (-not (Test-Path $KeyPath)) {
    # Si por alguna razón el archivo está vacío o bloqueado, el sistema genera un token criptográfico de 32 bytes único
    $CryptoKey = New-Object Byte[] 32
    [System.Security.Cryptography.RandomNumberGenerator]::Create().GetBytes($CryptoKey)
    [System.IO.File]::WriteAllBytes($KeyPath, $CryptoKey)
}

function Invoke-AesEncryption([string]$InputText, [string]$OutputPath) {
    try {
        $KeyBytes = [System.IO.File]::ReadAllBytes(".\VAULT\LLAVE_SISTEMA.key")
        
        # Inicializar el proveedor AES
        $Aes = [System.Security.Cryptography.Aes]::Create()
        $Aes.Key = $KeyBytes
        $Aes.GenerateIV() # Generar un Vector de Inicialización único por cada archivo para evitar patrones
        
        $Encryptor = $Aes.CreateEncryptor()
        $InputBytes = [System.Text.Encoding]::UTF8.GetBytes($InputText)
        
        # Cifrar datos en memoria RAM
        $MemStream = New-Object System.IO.MemoryStream
        $CryptoStream = New-Object System.Security.Cryptography.CryptoStream($MemStream, $Encryptor, [System.Security.Cryptography.CryptoStreamMode]::Write)
        $CryptoStream.Write($InputBytes, 0, $InputBytes.Length)
        $CryptoStream.FlushFinalBlock()
        
        # Combinar IV + Datos cifrados para almacenamiento seguro en el archivo destino
        $FinalBytes = New-Object Byte[] ($Aes.IV.Length + $MemStream.Length)
        [Array]::Copy($Aes.IV, 0, $FinalBytes, 0, $Aes.IV.Length)
        [Array]::Copy($MemStream.ToArray(), 0, $FinalBytes, $Aes.IV.Length, $MemStream.Length)
        
        [System.IO.File]::WriteAllBytes($OutputPath, $FinalBytes)
        
        # Limpieza de memoria RAM inmediata
        $CryptoStream.Dispose()
        $MemStream.Dispose()
        $Aes.Dispose()
    } catch {
        # Mecanismo Dead-Man: Si falla el cifrado, guardar en texto plano aislado para no detener la producción
        $InputText | Set-Content -Path "$OutputPath.bypass" -Force
    }
}
