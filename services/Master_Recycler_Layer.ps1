# -*- coding: utf-8 -*-
$ErrorActionPreference = "Stop"
Set-Location -Path "C:\NULOGIC_CORE"

function global:Invoke-SurgicalRecycler {
    $TimeStamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss.fff"
    $InitialRAM = [Math]::Round((Get-Process -Id $PID).WorkingSet64 / 1MB, 2)
    
    # 1. TRITURACIÓN DE BASURA BINARIA EN DISCO
    $TargetTrash = @("*.tmp", "*.bak", "*~*", "stress_*.json", "leak_*.tmp")
    foreach ($Pattern in $TargetTrash) {
        Get-ChildItem -Path "C:\NULOGIC_CORE\temp", "C:\NULOGIC_CORE\cache" -Filter $Pattern -Recurse -ErrorAction SilentlyContinue | ForEach-Object {
            try {
                [System.IO.File]::WriteAllBytes($_.FullName, (New-Object Byte[] 1024))
                Remove-Item -Path $_.FullName -Force -ErrorAction SilentlyContinue
            } catch {}
        }
    }

    # 2. TRUNCADO QUIRÚRGICO DE LOGS EXCEDENTES
    $LogFile = "C:\NULOGIC_CORE\logs\system.log"
    if (Test-Path $LogFile) {
        if ((Get-Item $LogFile).Length -gt 1MB) {
            $RotatedName = "C:\NULOGIC_CORE\archive\system_$(Get-Date -Format 'yyyyMMdd_HHmmss').log"
            Move-Item -Path $LogFile -Destination $RotatedName -Force -ErrorAction SilentlyContinue
            New-Item -ItemType File -Path $LogFile -Force | Out-Null
        }
    }

    # 3. RECICLAJE Y RE-UTILIZACIÓN DE MEMORIA RAM (.NET GARBAGE COLLECTOR)
    [System.GC]::Collect()
    [System.GC]::WaitForPendingFinalizers()
    
    $FinalRAM = [Math]::Round((Get-Process -Id $PID).WorkingSet64 / 1MB, 2)
    $SavedRAM = [Math]::Round($InitialRAM - $FinalRAM, 2)
    
    Write-Host "[$TimeStamp] [🧼][TokyoAI®] Limpieza de sustrato completada." -ForegroundColor Green
    Write-Host "       -> RAM Inicial: $InitialRAM MB | RAM Final: $FinalRAM MB | Reciclado: $SavedRAM MB" -ForegroundColor White
}

Remove-Item alias:purg-core -ErrorAction SilentlyContinue
New-Alias -Name "purg-core" -Value "Invoke-SurgicalRecycler" -Scope "Global" -Force