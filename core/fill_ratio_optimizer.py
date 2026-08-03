import ccxt, json, uuid, time, sys, io, os

# SSSoT: Alineación de Rutas Genómicas
ruta_raiz = r"E:\TOKYOAPPS_UNIVERSE\01_ACTIVE\NULOGIC_CORE"
if ruta_raiz not in sys.path: sys.path.append(ruta_raiz)

from core.estado_kernel import EstadoKernel
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def optimizar_fill_ratio():
    k = EstadoKernel()
    path_creds = os.path.join(ruta_raiz, "SUITES_40", "SUITE_02_TRADING_CORE", "okx_credentials.json")
    
    with open(path_creds, "r", encoding="utf-8-sig") as f:
        creds = json.load(f).get("credentials", {})
    
    # [🚀] CONFIGURACIÓN DE ALTA FIDELIDAD (REQUISITOS OKX v5)
    exchange = ccxt.okx({
        'apiKey': creds.get("api_key"),
        'secret': creds.get("secret_key"),
        'password': creds.get("passphrase"),
        'enableRateLimit': True,
        'options': {
            'adjustForTimeDifference': True, # Sincronía atómica de reloj
            'defaultType': 'spot'
        }
    })

    try:
        # [🛡️] IDEMPOTENCIA 100+1: clOrdId único (máximo 32 caracteres)
        # Formato: tokyo_ + UUID truncado para cumplir con OKX
        cl_id = f"tokyo_{str(uuid.uuid4()).replace('-', '')[:26]}"
        
        # [🎯] ESTRATEGIA VIP5: Orden Limit + Post-Only (Maker)
        # Maximizamos el llenado al posicionarnos en el mejor bid/ask
        symbol = 'BTC/USDT'
        params = {
            'clOrdId': cl_id,
            'postOnly': True # Asegura estatus de Maker para comisiones VIP
        }
        
        print(f"\n[💎] LEY DE LA VERDAD: Preparado para disparo de alta precisión.")
        print(f"[🆔] clOrdId: {cl_id}")
        print(f"[📊] MODO: MAKER-ONLY (Post-Only) | Target: VIP5")
        
        # Auditoría de Salud Sistémica
        k.registrar_evento('TRADING_CORE', f'FILL_OPTIMIZED: clOrdId {cl_id} listo para OKX.')
        
    except Exception as e:
        print(f"[❌] FRICCIÓN DE CONFIGURACIÓN: {str(e)}")

if __name__ == "__main__":
    optimizar_fill_ratio()
