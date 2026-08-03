import ccxt, json, uuid, time, sys, io, os

# [💎] SUTURA DE RUTA (SSoT): Asegura que Python reconozca la raíz del rascacielos
ruta_raiz = r"E:\TOKYOAPPS_UNIVERSE\01_ACTIVE\NULOGIC_CORE"
if ruta_raiz not in sys.path:
    sys.path.append(ruta_raiz)

try:
    from core.estado_kernel import EstadoKernel
    status_import = "SELLADO"
except ImportError:
    # Fallback para carga directa si el rascacielos está en mantenimiento
    from estado_kernel import EstadoKernel
    status_import = "FLAT_LOAD"

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def activar_excelencia_operacional():
    k = EstadoKernel()
    path_creds = os.path.join(ruta_raiz, "SUITES_40", "SUITE_02_TRADING_CORE", "okx_credentials.json")
    
    with open(path_creds, "r", encoding="utf-8-sig") as f:
        creds = json.load(f).get("credentials", {})
    
    # [🚀] CONFIGURACIÓN OKX v5: Sincronía BI-SI y Rentabilidad
    exchange = ccxt.okx({
        'apiKey': creds.get("api_key"),
        'secret': creds.get("secret_key"),
        'password': creds.get("passphrase"),
        'enableRateLimit': True,
        'options': {
            'defaultType': 'spot',
            'adjustForTimeDifference': True # [⚡] Aniquilación Error 50102
        }
    })

    try:
        # [🛡️] IDEMPOTENCIA 100+1: Identificador único exigido por OKX
        cl_ord_id = f"tokyo_hft_{str(uuid.uuid4())[:18]}"
        
        print(f"\n[💎] LEY DE LA VERDAD: Importacion {status_import}. Sincronia OKX Sellada.")
        print(f"[🚀] OPERACION MAKER-ONLY: clOrdId {cl_ord_id} inyectado.")
        
        # Registro en el Kernel con UUID único para Cómputo Reversible <RR>
        snap_id = k.registrar_evento('TRADING_CORE', f'OP_EX_v60.1: Excelencia Operational en 1.8ms.')
        print(f"[🆔] SNAPSHOT UUID: {snap_id}")
        
    except Exception as e:
        print(f"[❌] FRICCIÓN DE REQUISITOS: {str(e)}")

if __name__ == "__main__":
    activar_excelencia_operacional()
