$ErrorActionPreference = "Stop"
Set-Location -Path "C:\NULOGIC_CORE"

function Scan-Inbox-For-Voice {
    $TargetTask = ".\inbox\Active_Task_BI-SI.json"
    $VoiceLog = ".\logs\system.log"
    
    # Si TokyoAI® acaba de enrutar una tarea descifrada al inbox, el motor de voz la asimila
    if (Test-Path $TargetTask) {
        try {
            $TaskData = Get-Content $TargetTask | ConvertFrom-Json
            
            # Extraer variables para el VoiceStudio
            $Status = $TaskData.bisi_status
            $Signal = $TaskData.alpha_signal
            
            # Registrar el hito en UTF-8 inmutable para el componente web
            $TimeStamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
            $LogEntry = "[$TimeStamp] [RESONANCIA] Canalizando hito BI-SI a VoiceStudio. Estatus: $Status | Alfa: $Signal"
            Add-Content -Path $VoiceLog -Value $LogEntry
            
            # Emitir tono de confirmación molecular (Frecuencia armónica de éxito)
            [Console]::Beep(1800, 100)
            [Console]::Beep(2200, 150)
            
            Write-Output "[🎙️][BI-SI] Datos integrados al canal de voz de forma automatizada."
        } catch {
            # Mitigación anti-lag instantánea
        }
    }
}
Scan-Inbox-For-Voice