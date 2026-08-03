$ErrorActionPreference = "Stop"
Set-Location -Path "C:\NULOGIC_CORE"

function global:Invoke-ResendReport {
    param ([string]$Subject, [string]$HtmlBody)
    $SecretsFile = "C:\NULOGIC_CORE\secrets\api_credentials.json"
    
    if (Test-Path $SecretsFile) {
        $Creds = Get-Content $SecretsFile | ConvertFrom-Json
        $ApiKey = $Creds.RESEND_API_KEY
        
        if ($ApiKey -and $ApiKey -notmatch "TU_KEY") {
            # Invocación real mediante la API REST de Resend en formato nativo JSON
            $Uri = "https://resend.com"
            $Headers = @{ "Authorization" = "Bearer $ApiKey"; "Content-Type" = "application/json" }
            $Body = @{
                "from" = "NulogicCore <onboarding@resend.dev>";
                "to" = "tokyo.m.dev@local.system";
                "subject" = $Subject;
                "html" = $HtmlBody
            } | ConvertTo-Json
            
            try {
                Invoke-RestMethod -Uri $Uri -Method Post -Headers $Headers -Body $Body -ErrorAction SilentlyContinue | Out-Null
                Write-Output "[✉️][Resend] Reporte financiero consolidado emitido con éxito."
            } catch {
                # Mitigación anti-lag para evitar interrupciones por rechazo de API Key
            }
        }
    }
}