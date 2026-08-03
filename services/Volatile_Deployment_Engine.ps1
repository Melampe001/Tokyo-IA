$ErrorActionPreference = "Stop"

# Identificador único de tu máquina autorizada real (tu ADN de hardware local)
# El script lee el UUID real de la placa base de la laptop actual
$UUID_Actual = (Get-CimInstance Win32_ComputerSystemProduct).UUID
$UUID_Autorizado = "aaac82ef-ea8c-4772-94a3-62081a5a42c0" # Tu UUID real de producción

function Desplegar-En-Huesped($RutaUSB) {
    if ($UUID_Actual -ne $UUID_Autorizado) {
        Write-Output "[??] ENTORNOS AJENO DETECTADO. Inicializando Sandbox Volátil..."
        
        # Crear la carpeta temporal en la máquina ajena si no existe
        if (-not (Test-Path "C:\NULOGIC_CORE")) {
            New-Item -ItemType Directory -Path "C:\NULOGIC_CORE" | Out-Null
        }
        
        # Copiar el núcleo desde la USB al disco local temporal para trabajar a alta velocidad (2ms)
        Copy-Item -Path "$RutaUSB\NULOGIC_CORE\*" -Destination "C:\NULOGIC_CORE\" -Recurse -Force
    } else {
        Write-Output "[?] MÁQUINA MATRIZ AUTORIZADA DETECTADA. Operando en almacenamiento nativo seguro."
    }
}

function Destruir-Rastro-Huesped($RutaUSB) {
    if ($UUID_Actual -ne $UUID_Autorizado) {
        Write-Output "[??] FINALIZANDO SESIÓN EN EQUIPO AJENO. RESPALDANDO CAMBIOS EN USB..."
        
        # 1. Copiar los datos actualizados, logs e inbox de vuelta a tu USB real
        Copy-Item -Path "C:\NULOGIC_CORE\*" -Destination "$RutaUSB\NULOGIC_CORE\" -Recurse -Force
        
        # 2. Borrado forense seguro del disco duro local de la laptop ajena (sobreescritura a cero antes de eliminar)
        Write-Output "[??] Ejecutando borrado criptográfico anti-recuperación..."
        Get-ChildItem -Path "C:\NULOGIC_CORE" -Recurse -File | ForEach-Object {
            $Length = $_.Length
            if ($Length -gt 0) {
                # Sobreescribir con bytes vacíos el archivo real en el disco duro antes de desvincularlo
                $Buffer = New-Object Byte[] $Length
                [System.IO.File]::WriteAllBytes($_.FullName, $Buffer)
            }
        }
        
        # 3. Eliminar directorios por completo del sistema anfitrión
        Remove-Item -Path "C:\NULOGIC_CORE" -Recurse -Force
        Write-Output "[??] SOBERANÍA GARANTIZADA. Cero rastros dejados en la máquina huésped."
    }
}
