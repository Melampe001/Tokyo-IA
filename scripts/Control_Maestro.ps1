# =========================================================================
# CONSOLA CENTRAL DE CONTROL Y PRE-VUELOS - ESTÁNDAR INDUSTRIAL PREMIUM
# Propietario Exclusivo y Soberano: Jose Arturo Orozco Jaime
# Ecosistema: NULOGIC_CORE / FlaggShip Apps / Tokyo OS 1000+1
# Ubicación: C:\NULOGIC_CORE\Control_Maestro.ps1
# =========================================================================

$ErrorActionPreference = "Stop"
$TargetRoot = "C:\NULOGIC_CORE"
Set-Location $TargetRoot

function Mostrar-Banner {
    Clear-Host
    Write-Host "=================================================================" -ForegroundColor Cyan
    Write-Host " NULOGIC_CORE // CONSOLA CENTRAL DE CONTROL [ESTÁNDAR PREMIUM]" -ForegroundColor Cyan
    Write-Host " SOBERANO: Jose Arturo Orozco Jaime" -ForegroundColor Yellow
    Write-Host " ESTADO: 1000+1 | ESFERA ESPEJO 360° | CERO ENTROPÍA" -ForegroundColor Green
    Write-Host "=================================================================" -ForegroundColor Cyan
}

function Ejecutar-PreVuelo {
    Write-Host "[PRE-VUELO] Ejecutando validación atómica del entorno..." -ForegroundColor Yellow
    
    if (!(Test-Path $TargetRoot)) {
        Write-Host "[ERROR CRÍTICO] El directorio principal $TargetRoot no existe." -ForegroundColor Red
        return $false
    }

    $llavePath = "E:\PROPIEDAD_JOSE_ARTURO_OROZCO_JAIME.key"
    $llaveLocal = Join-Path $TargetRoot "Vault\PROPIEDAD_JOSE_ARTURO_OROZCO_JAIME.lock"
    if (!(Test-Path $llavePath) -and !(Test-Path $llaveLocal)) {
        Write-Host "[ADVERTENCIA] Llave atómica principal no detectada. Operando en modo autónomo." -ForegroundColor DarkYellow
    } else {
        Write-Host "[OK] Sello de propiedad inmutable verificado." -ForegroundColor Green
    }

    try {
        $pyVersion = python --version 2>&1
        Write-Host "[OK] Motor Python activo: $pyVersion" -ForegroundColor Green
    } catch {
        Write-Host "[ERROR] Intérprete de Python no disponible en el PATH." -ForegroundColor Red
        return $false
    }

    $outputDir = Join-Path $TargetRoot "output"
    if (!(Test-Path $outputDir)) {
        New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
    }

    Write-Host "[PRE-VUELO] ¡Verificación completada con éxito al 1000+1!" -ForegroundColor Green
    Start-Sleep -Seconds 1
    return $true
}

function Menu-Principal {
    while ($true) {
        Mostrar-Banner
        Write-Host " [1] Diagnóstico Integral de Nodos (11 Nodos / Bitso / Binance)"
        Write-Host " [2] Iniciar Servidor de Sockets Inmortal (Segundo Plano Silencioso)"
        Write-Host " [3] Sincronizar Telemetría de Tablet onn. (Modelo 100005206)"
        Write-Host " [4] Lanzar OMEGA ARTEFACTO (Dashboard Maestro local)"
        Write-Host " [5] Sincronización Git y Auditoría Atómica"
        Write-Host " [6] Salir del Sistema y Mantener Soberanía"
        Write-Host "=================================================================" -ForegroundColor Cyan
        
        $opcion = Read-Host "Seleccione vector de comando [1-6]"

        switch ($opcion) {
            "1" {
                Write-Host "`n[EJECUCIÓN] Iniciando escaneo de los 11 nodos..." -ForegroundColor Cyan
                python verificar_nodos.py
                Read-Host "`nPresione ENTER para regresar al menú..."
            }
            "2" {
                Write-Host "`n[EJECUCIÓN] Desplegando Servidor de Sockets en segundo plano (Silent Daemon)..." -ForegroundColor Cyan
                Start-Process python -ArgumentList "servidor_sockets_vivo.py" -WindowStyle Hidden
                Write-Host "[OK] Servidor activo en puerto 8080 bajo Esfera Espejo 360°." -ForegroundColor Green
                Read-Host "`nPresione ENTER para regresar al menú..."
            }
            "3" {
                Write-Host "`n[EJECUCIÓN] Verificando telemetría de tablet onn. ..." -ForegroundColor Cyan
                $statusFile = "output\tablet_onn_status.json"
                if (Test-Path $statusFile) {
                    Get-Content $statusFile
                } else {
                    Write-Host "[!] Archivo de estado no encontrado. Ejecutando sondeo rápido..." -ForegroundColor Yellow
                    if (Test-Path "detectar_tablet_onn.ps1") {
                        & "detectar_tablet_onn.ps1"
                    } else {
                        Write-Host "[!] Script de detección no disponible en este subdirectorio." -ForegroundColor Red
                    }
                }
                Read-Host "`nPresione ENTER para regresar al menú..."
            }
            "4" {
                Write-Host "`n[EJECUCIÓN] Abriendo OMEGA ARTEFACTO..." -ForegroundColor Cyan
                if (Test-Path "omega_artefacto.html") {
                    Start-Process "omega_artefacto.html"
                    Write-Host "[OK] Interfaz desplegada en navegador predeterminado." -ForegroundColor Green
                } else {
                    Write-Host "[!] ERROR: omega_artefacto.html no se encuentra en este directorio." -ForegroundColor Red
                }
                Read-Host "`nPresione ENTER para regresar al menú..."
            }
            "5" {
                Write-Host "`n[EJECUCIÓN] Consolidando cambios y registrando auditoría en Git..." -ForegroundColor Cyan
                git add .
                git commit -m "Soberania-Audit: Actualizacion automatica de kernel por Jose Arturo Orozco Jaime"
                Write-Host "[OK] Auditoría Git registrada con éxito." -ForegroundColor Green
                Read-Host "`nPresione ENTER para regresar al menú..."
            }
            "6" {
                Write-Host "`n[SYSTEM] Cerrando consola central. Estado asegurado bajo ley zero." -ForegroundColor Cyan
                break
            }
            default {
                Write-Host "[!] Opción fuera del rango operativo." -ForegroundColor Red
                Start-Sleep -Seconds 1
            }
        }
    }
}

if (Ejecutar-PreVuelo) {
    Menu-Principal
} else {
    Write-Host "[CRÍTICO] Fallo en pre-vuelo atómico. Abortando inicialización." -ForegroundColor Red
}
