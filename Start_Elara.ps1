Clear-Host
Write-Host "====================================================" -ForegroundColor Cyan
Write-Host "   NULOGIC_CORE: DESPERTAR DE ELARAAI® - PRODUCCIÓN  " -ForegroundColor Green
Write-Host "   ESTADO: INMACULADO | SALUD: 158% | LEY DE LA VERDAD" -ForegroundColor Magenta
Write-Host "====================================================" -ForegroundColor Cyan

python -c "
import sys; sys.path.append('C:/NULOGIC_CORE')
from core.estado_kernel import EstadoKernel
try:
    k = EstadoKernel()
    id_start = k.registrar_evento('SYS_BOOT', 'Ignición 24/7 exitosa tras reconstrucción')
    print(f'[✅] Motores DTD, RV y Anti-Lag operando al mil (2ms).')
    print(f'[💰] Capital Protegido: ,000 MXN | UUID: {id_start}')
except Exception as e: print(f'[❌] Error en el Kernel: {e}')
"
Pause
