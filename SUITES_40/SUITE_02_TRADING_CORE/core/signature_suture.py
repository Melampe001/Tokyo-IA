import ccxt, json, os, sys, io

# Forzar streams a UTF-8 sin errores
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def aplicar_sutura_firma():
    path = r"E:\TOKYOAPPS_UNIVERSE\01_ACTIVE\NULOGIC_CORE\SUITES_40\SUITE_02_TRADING_CORE\okx_credentials.json"
    
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
    except Exception as e:
        print(f"[❌ ERROR DE LECTURA]: {e}")
        return
    
    creds = data.get("credentials", {})
    api_key = creds.get("api_key")
    secret_key = creds.get("secret_key")
    passphrase = creds.get("passphrase")

    if not secret_key or "INTRODUZCA" in secret_key:
        print("[❌] ERROR: Secret Key no válida o ausente.")
        return

    exchange = ccxt.okx({
        'apiKey': api_key,
        'secret': secret_key,
        'password': passphrase,
        'enableRateLimit': True,
        'options': {'defaultType': 'swap'}
    })

    try:
        # Validación de Sincronía Neural (Handshake OKX)
        balance = exchange.fetch_balance()
        print("[✅] SUTURA EXITOSA: Firma HMAC validada bajo SSoT (Error 50113 aniquilado).")
        total_usdt = balance.get('total', {}).get('USDT', balance.get('total', {}).get('USD', 0))
        print(f"[📊] BALANCE TOTAL DETECTADO:  USDT")
    except Exception as e:
        print(f"[⚠️] FRICCIÓN PERSISTENTE: {str(e)}")

if __name__ == "__main__":
    aplicar_sutura_firma()