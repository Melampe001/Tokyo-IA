# TOKYO OS (c) 2026 - TODOS LOS DERECHOS RESERVADOS - MARCA REGISTRADA
import os, json, ccxt

def sutura_autenticacion_segura():
    cred_path = r"E:\TOKYOAPPS_UNIVERSE\01_ACTIVE\NULOGIC_CORE\SUITES_40\SUITE_02_TRADING_CORE\okx_credentials.json"
    
    if not os.path.exists(cred_path):
        print(f"[❌] ERROR: No se detecta el ADN de credenciales.")
        return

    # SUTURA CRÍTICA: 'utf-8-sig' elimina el BOM invisible automáticamente
    try:
        with open(cred_path, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
    except Exception as e:
        print(f"[❌] FALLO LÓGICO DE LECTURA: {e}")
        return
    
    creds = data.get("credentials", {})
    api_key = creds.get("api_key", "").strip()
    secret = creds.get("secret_key", "").strip()
    passphrase = creds.get("passphrase", "").strip()

    if not all([api_key, secret, passphrase]):
        print("[⚠️] ALERTA: Token de acceso incompleto.")
        return

    # Inicialización del Exchange (Determinismo Absoluto)
    exchange = ccxt.okx({
        'apiKey': api_key,
        'secret': secret,
        'password': passphrase,
        'enableRateLimit': True
    })

    try:
        balance = exchange.fetch_balance()
        print("\n" + "="*50)
        print("   SINCRO-RELOJ VALIDADA - ACCESO SOBERANO")
        print("="*50)
        print(f"[✅] INTEGRIDAD COGNITIVA: 100%")
        print(f"[💰] TOTAL USDT: ${balance.get('total', {}).get('USDT', '0.00')}")
        print("="*50)

    except Exception as e:
        print(f"\n[❌] FRICCIÓN EN EXCHANGE: {str(e)}")

if __name__ == "__main__":
    sutura_autenticacion_segura()

