$ErrorActionPreference = "Stop"
Set-Location -Path "C:\NULOGIC_CORE"

function global:Ejecutar-Simulacro-Entrenamiento {
    param (
        [ValidateSet("CorromperLog", "SimularFugaMemoria", "RomperRuta", "SimularSabotajeCodigo", "SaturarInbox")]
        [string]$TipoFalla
    )
    
    $LogFile = "C:\NULOGIC_CORE\logs\system.log"
    $TimeStamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss.fff"
    
    Write-Host "`n[🔥][CAOS] Inyectando contingencia real: $TipoFalla..." -ForegroundColor Yellow
    
    switch ($TipoFalla) {
        "CorromperLog" {
            Add-Content -Path $LogFile -Value "[$TimeStamp] [CRITICAL] ALERTA: CRITICAL_CAPITAL_DROP DETECTADO."
            Write-Host "  [⚡] Anomalía de capital simulada con éxito." -ForegroundColor DarkYellow
        }
        "SimularFugaMemoria" {
            $Buffer = New-Object Byte[] 1024
            for ($i=0; $i -lt 50; $i++) {
                [System.IO.File]::WriteAllBytes("C:\NULOGIC_CORE\temp\leak_$i.tmp", $Buffer)
            }
            Write-Host "  [⚡] Muestras de estrés inyectadas en RAM/Disco de forma ultra rápida." -ForegroundColor DarkYellow
        }
        "RomperRuta" {
            Set-Location -Path "C:\WINDOWS\system32"
            Write-Host "  [⚡] Contexto movido a System32." -ForegroundColor DarkYellow
        }
        "SimularSabotajeCodigo" {
            # Inyectar una línea corrupta en un script secundario para forzar la auto-sanación por Git
            Add-Content -Path "C:\NULOGIC_CORE\services\NTFS_Shield_Engine.ps1" -Value "`n# CODI_CORRUPTO_ERROR"
            Write-Host "  [⚡] Modificación no autorizada realizada en el código de seguridad." -ForegroundColor DarkYellow
        }
        "SaturarInbox" {
            # Simular ráfaga masiva de 500 solicitudes simuladas en el inbox de golpe
            $Payload = @{"intent_raw"="PROCESAR_ALTA_FRECUENCIA"} | ConvertTo-Json
            for ($i=0; $i -lt 500; $i++) {
                [System.IO.File]::WriteAllText("C:\NULOGIC_CORE\inbox\STRESS_$i.json", $Payload, [System.Text.Encoding]::UTF8)
            }
            Write-Host "  [⚡] Inundación de buffer inyectada en el /inbox/ real." -ForegroundColor DarkYellow
        }
    }
    
    # Pausa de procesamiento y relanzamiento del control maestro para auto-sanar
    Start-Sleep -Milliseconds 100
    Set-Location -Path "C:\NULOGIC_CORE"
    . "C:\NULOGIC_CORE\Bootstrap_Core.ps1"
}

Remove-Item alias:run-chaos -ErrorAction SilentlyContinue
New-Alias -Name "run-chaos" -Value "Ejecutar-Simulacro-Entrenamiento" -Scope "Global" -Force