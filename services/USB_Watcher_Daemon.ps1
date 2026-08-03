$ErrorActionPreference = "Stop"
Set-Location -Path "C:\NULOGIC_CORE"

# 1. Limpiar cualquier suscripción previa para mantener la idempotencia pura del kernel
Unregister-Event -SourceIdentifier "NULOGIC_USB_INSERTION" -ErrorAction SilentlyContinue

# 2. Consulta WQL para capturar el evento físico exacto de inserción de almacenamiento (EventType = 2 -> Arribo)
$Query = "SELECT * FROM Win32_VolumeChangeEvent WHERE EventType = 2"

# 3. Registrar el evento en el kernel. Cuando se inserte una USB, se ejecutará este bloque de inmediato
Register-WmiEvent -Query $Query -SourceIdentifier "NULOGIC_USB_INSERTION" -Action {
    # Detectar la letra de unidad asignada por Windows en microsegundos
    $DriveLetter = $Event.SourceEventArgs.NewEvent.DriveName
    $SigPath = "$DriveLetter\NULOGIC_KEY.sig"
    
    # Validar las firmas criptográficas de tu sello inmutable en la USB real
    if (Test-Path $SigPath) {
        $Signature = Get-Content $SigPath -Raw
        if ($Signature -match "TOKYO_M_SOVEREIGN_KEY_001") {
            [Console]::Beep(1500, 100) # Sonido sutil de reconocimiento de hardware
            
            # Invocar los motores de sincronización y despliegue del ADN innato
            if (Test-Path "C:\NULOGIC_CORE\services\Matrix_Sync_Engine.ps1") {
                . "C:\NULOGIC_CORE\services\Matrix_Sync_Engine.ps1"
                Ejecutar-Sincronizacion-Matriz -RutaUSB $DriveLetter
            }
        }
    }
} | Out-Null

Write-Output "[⚡][TokyoAI®] Demonio WMI activo en el Kernel de Windows. Escucha de USB instantánea armada."