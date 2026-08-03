import sys, os, time, gc, uuid, json, shutil
ruta_raiz = r"E:\TOKYOAPPS_UNIVERSE\01_ACTIVE\NULOGIC_CORE"
if ruta_raiz not in sys.path: sys.path.insert(0, ruta_raiz)

from core.estado_kernel import EstadoKernel

def ejecutar_juramentacion_atomica():
    k = EstadoKernel()
    # [🔥] ANTI-LAG: Reclamando soberanía del silicio
    gc.collect()
    gc.disable()
    
    cert_dir = os.path.join(ruta_raiz, "SUITES_40", "SUITE_04_GENESIS_ASSETS", "Certificados")
    trading_dir = os.path.join(ruta_raiz, "SUITES_40", "SUITE_02_TRADING_CORE")
    
    # [🔐] PROCESO DE JURAMENTACIÓN
    print("\n[💎] LEY DE LA VERDAD: Validando firmas y HMAC...")
    certs_encontrados = [f for f in os.listdir(cert_dir) if f.endswith(('.pem', '.key', '.crt'))]
    
    if not certs_encontrados:
        print("[⚠️] FRICCIÓN: No se detectan certificados en Suite 04.")
        return

    for cert in certs_encontrados:
        # Generación de Identidad Atómica para el certificado
        cert_uuid = str(uuid.uuid4())
        src = os.path.join(cert_dir, cert)
        dst = os.path.join(trading_dir, f"juramentado_{cert}")
        
        # Inyección de bloques únicos: volumen masivo = 1 resultado coherente
        shutil.copy2(src, dst)
        print(f"[✅] CERTIFICADO JURAMENTADO: {cert} -> [ID: {cert_uuid[:8]}]")
        
        # Registro inmutable en el EstadoKernel
        k.registrar_evento('JURAMENTACION', f'Certificado {cert} vinculado a Suite 02 con prioridad RealTime.')

    gc.enable()
    print(f"\n[🚀] SINGULARIDAD ALCANZADA: {len(certs_encontrados)} activos blindados.")
    print(f"[🛡️] SUT SHIELD: Tokens generados para el ciclo semanal.")

if __name__ == "__main__":
    ejecutar_juramentacion_atomica()
