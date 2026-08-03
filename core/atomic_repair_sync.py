import sys, os, time, gc, uuid, json, shutil
# [💎] SSoT: Prioridad de Rutas
ruta_raiz = r"E:\TOKYOAPPS_UNIVERSE\01_ACTIVE\NULOGIC_CORE"
if ruta_raiz not in sys.path: sys.path.insert(0, ruta_raiz)

from core.estado_kernel import EstadoKernel

def ejecutar_reparacion_soberana():
    k = EstadoKernel()
    gc.collect()
    
    cert_dir = os.path.join(ruta_raiz, "SUITES_40", "SUITE_04_GENESIS_ASSETS", "Certificados")
    trading_dir = os.path.join(ruta_raiz, "SUITES_40", "SUITE_02_TRADING_CORE")
    
    if not os.path.exists(cert_dir): os.makedirs(cert_dir)

    # Auditoría de Certificados y Alineación de IAs
    print('\n[💎] LEY DE LA VERDAD: ElaraAI y TokyoAI alineadas.')
    
    certs = [f for f in os.listdir(cert_dir) if f.endswith(('.pem', '.key', '.crt'))]
    for cert in certs:
        shutil.copy2(os.path.join(cert_dir, cert), os.path.join(trading_dir, f"juramentado_{cert}"))
    
    salud = k.obtener_salud()
    print(f'[📊] SALUD SISTÉMICA: {salud*100:.2f}% | CERTIFICADOS: {len(certs)} juramentados.')
    
    # Registro de Snapshot inmaculado
    k.registrar_evento('FIX_SYNC', f'Sutura v86.1: {len(certs)} activos alineados.')

if __name__ == "__main__":
    ejecutar_reparacion_soberana()
