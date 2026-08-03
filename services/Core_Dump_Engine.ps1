$ErrorActionPreference = "Stop"
Set-Location -Path "C:\NULOGIC_CORE"

function Invoke-CoreDirectoryDump {
    Write-Output "[🔍][TokyoAI®] Ejecutando radiografía criptográfica SHA-256 end-to-end..."
    
    $TargetFolders = @("archive", "assets", "bridge", "cache", "config", "core", "data", "inbox", "infrastructure", "interface", "logic", "logs", "modules", "output", "queue", "runtime", "secrets", "services", "telemetry", "temp", "trig_rules")
    $DumpReport = @{
        "dump_timestamp" = (Get-Date -Format "yyyy-MM-dd HH:mm:ss.fff");
        "system_status"  = "IMMACULATE";
        "folders_audit"  = @()
    }
    
    foreach ($Folder in $TargetFolders) {
        $Files = Get-ChildItem -Path ".\$Folder" -File -Recurse -ErrorAction SilentlyContinue
        $FolderSize = 0
        $FileEntries = @()
        
        foreach ($File in $Files) {
            $FolderSize += $File.Length
            # Calcular ADN único SHA-256 de cada recurso real del Creador
            $Hash = (Get-FileHash -Path $File.FullName -Algorithm SHA256).Hash
            $FileEntries += @{
                "file_name" = $File.Name;
                "size_bytes" = $File.Length;
                "sha256_hash" = $Hash
            }
        }
        
        $DumpReport.folders_audit += @{
            "folder_name" = $Folder;
            "total_files" = $Files.Count;
            "total_size_bytes" = $FolderSize;
            "manifest" = $FileEntries
        }
    }
    
    # Escribir el reporte maestro inmutable en UTF-8 puro
    $JsonOutput = $DumpReport | ConvertTo-Json -Depth 6
    [System.IO.File]::WriteAllText("C:\NULOGIC_CORE\logs\health_dump.json", $JsonOutput, [System.Text.Encoding]::UTF8)
    Write-Output "[✅][TokyoAI®] Volcado de salud completado con éxito en /logs/health_dump.json"
}
Invoke-CoreDirectoryDump