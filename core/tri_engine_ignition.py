import sys
import os
import importlib
import time
import json
import io
import ccxt

if 'queue' in sys.modules:
    del sys.modules['queue']

import queue
importlib.reload(queue)

PROJECT_ROOT = r"E:\TOKYOAPPS_UNIVERSE\01_ACTIVE\NULOGIC_CORE"
if PROJECT_ROOT in sys.path:
    sys.path.remove(PROJECT_ROOT)
sys.path.insert(0, PROJECT_ROOT)

from core.estado_kernel import EstadoKernel

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def ejecutar_automatizacion_v22():
    k = EstadoKernel()
    
    apiKey = r"f363835e-3357-464c-985d-1d5227607df1"
    secret = r"CONSERVADA"
    password = r"#Zeekr002"

    exchange = ccxt.okx({
        'apiKey': apiKey,
        'secret': secret,
        'password': password,
        'enableRateLimit': True,
        'options': {
            'defaultType': 'swap',
            'adjustForTimeDifference': True
        }
    })

    exchange.set_sandbox_mode(False)

    try:
        print("[🔎 DIAGNÓSTICO #Zeekr002] Sincronizando reloj NTP con OKX Live...")
        server_time = exchange.fetch_time()
        print(f"[⏱️ NTP SYNC OK] Servidor OKX Live: {server_time}")

        print("[🚀 DISPARO PRIVADO AUTOMATIZADO] Solicitando balance de cuenta...")
        balance = exchange.fetch_balance()
        usdt_free = balance.get('free', {}).get('USDT', 0)
        
        print(f"[💎 MONETIZACIÓN ACTIVA #Zeekr002] Firma HMAC v5 APROBADA. USDT Libre: {usdt_free}")
        k.registrar_evento('PREVUELO_V22', 'AUTOMATIZACIÓN_Y_DISPAROS_EN_VIVO_OPERATIVOS')

    except ccxt.AuthenticationError as e:
        print(f"\n[❌ ERROR 50113 PERSISTENTE]: {e}")
        print("="*70)
        print("VERIFICACIÓN DE PROTOCOLO #Zeekr002:")
        print("Si el Secret Key ingresado sigue teniendo menos de 30 caracteres, OKX rechaza la firma.")
        print("Asegúrate de copiar íntegramente la clave secreta desde el panel web de OKX.")
        print("="*70)
    except Exception as e:
        print(f"[❌ ERROR NO CONTROLADO]: {str(e)}")

if __name__ == "__main__":
    ejecutar_automatizacion_v22()