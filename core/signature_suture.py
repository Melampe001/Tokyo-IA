import ccxt, json, os, sys, io
from core.estado_kernel import EstadoKernel

def aplicar_sutura_firma():
    k = EstadoKernel()
    path = r"E:\TOKYOAPPS_UNIVERSE\01_ACTIVE\NULOGIC_CORE\SUITES_40\SUITE_02_TRADING_CORE\okx_credentials.json"
    
    with open(path, "r", encoding="utf-8-sig") as f:
        data = json.load(f)
    
    creds = data.get("credentials", {})
    api_key = creds.get("api_key")
    passphrase = creds.get("passphrase")

    # [💎] SUTURA CRÍTICA: Sustituya el texto de abajo por su SECRET KEY REAL
    secret_key = "INTRODUZCA_AQUÍ_SU_SECRET_KEY_REAL" 

    if "INTRODUZCA" in secret_key:
        print("[❌] ERROR: El sistema detecta un marcador de posicion. Inyecte la llave real.")
        return

    exchange = ccxt.okx({
        'apiKey': api_key,
        'secret': secret_key,
        'password': passphrase,
        'enableRateLimit': True,
        'options': {'defaultType': 'spot'}
    })

    try:
        # Validación de Sincronía Neural (Handshake) [3]
        balance = exchange.fetch_balance()
        print(f"[✅] SUTURA EXITOSA: Firma validada bajo SSoT.")
        print(f"[📊] BALANCE USDT DETECTADO: {balance['total'].get('USDT', 0)}")
        
        # Registro de Snapshot Inmaculado [4]
        k.registrar_evento('SURGICAL_HUB', 'Sello v51.1: Error 50113 aniquilado.')
    except Exception as e:
        print(f"[⚠️] FRICCIÓN PERSISTENTE: {str(e)}")

if __name__ == "__main__":
    aplicar_sutura_firma()
