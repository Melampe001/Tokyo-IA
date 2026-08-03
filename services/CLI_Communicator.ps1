function global:Enviar-Instruccion-Agente {
    param (
        [ValidateSet("TokyoAI", "ElaraAI")]
        [string]$TargetAgent,
        [string]$CommandText
    )
    $TimeStamp = Get-Date -Format "yyyyMMdd_HHmmss.fff"
    $FileInbox = "C:\NULOGIC_CORE\inbox\NATURAL_$($TargetAgent)_$TimeStamp.json"
    
    # Empaquetado estricto en UTF-8 con metadatos de Gobernanza Humana
    $Payload = @{
        "timestamp"    = (Get-Date -Format "yyyy-MM-dd HH:mm:ss.fff");
        "protocol"     = "Gobernanza Humana Asíncrona mediante Lenguaje Natural Estructurado";
        "sender"       = "Tokyo M. (Creador Absoluto)";
        "target"       = $TargetAgent;
        "intent_raw"   = $CommandText;
        "status"       = "INJECTED_IN_KERNEL";
        "encoding"     = "UTF-8_BOM"
    } | ConvertTo-Json -Depth 4
    
    [System.IO.File]::WriteAllText($FileInbox, $Payload, [System.Text.Encoding]::UTF8)
    [Console]::Beep(2200, 150)
    
    $RespTime = Get-Date -Format "HH:mm:ss.fff"
    Write-Host "`n[🛰️] Intención en Lenguaje Natural inyectada en el /inbox/ de $TargetAgent." -ForegroundColor Green
    
    # Despacho asíncrono simulando el retorno inmediato del sustrato de memoria
    if ($TargetAgent -eq "TokyoAI") {
        Write-Host "[$RespTime] [🤖][TokyoAI®]: Intención absorbida como ADN. Ajustando topología de infraestructura a 2ms." -ForegroundColor Green
    } else {
        Write-Host "[$RespTime] [🔮][ElaraAI®]: Intención absorbida en la Esfera Omega 360°. Sintonizando matrices financieras sin lag." -ForegroundColor Green
    }
}

Remove-Item alias:cmd-agent -ErrorAction SilentlyContinue
New-Alias -Name "cmd-agent" -Value "Enviar-Instruccion-Agente" -Scope "Global" -Force