# TOKYO OS (c) 2026 - TODOS LOS DERECHOS RESERVADOS - MARCA REGISTRADA
import os, json

credential_paths = [
    "okx_credentials.json",
    "../okx_credentials.json",
    r"E:\TOKYOAPPS_UNIVERSE\01_ACTIVE\NULOGIC_CORE\SUITES_40\SUITE_02_TRADING_CORE\okx_credentials.json"
]

config = None
found_path = None
for path in credential_paths:
    if os.path.exists(path):
        found_path = path
        with open(path, "r", encoding="utf-8") as f:
            config = json.load(f)
        break

if not config:
    print("[ERROR CRÍTICO] No se encontró el archivo 'okx_credentials.json'.")
    exit(1)

print(f"[INFO] Archivo localizado en: {found_path}")
creds = config.get("credentials", {})

# Verificar campos comunes o alternativas si la llave está mal nombrada
api_key = creds.get("api_key", creds.get("apiKey", ""))
secret_key = creds.get("secret_key", creds.get("secret", ""))
passphrase = creds.get("passphrase", creds.get("password", ""))

print(f" - API Key    : {'[OK]' if api_key else '[FALTA]'}")
print(f" - Secret Key : {'[OK]' if secret_key else '[FALTA]'}")
print(f" - Passphrase : {'[OK]' if passphrase else '[FALTA]'}")

if not passphrase:
    print("\n[⚠️] El campo 'passphrase' no se encuentra dentro del bloque 'credentials'.")
    print("Por favor, asegúrate de que tu archivo 'okx_credentials.json' tenga esta estructura exacta:")
    print('''
{
  "exchange": "okx",
  "credentials": {
    "api_key": "TU_API_KEY",
    "secret_key": "TU_SECRET_KEY",
    "passphrase": "TU_PASSPHRASE"
  }
}
    ''')
else:
    print("\n[✅] Estructura de credenciales validada con éxito. Procediendo a verificar con CCXT...")
    import ccxt
    exchange = ccxt.okx({
        'apiKey': api_key,
        'secret': secret_key,
        'password': passphrase,
        'enableRateLimit': True,
        'options': {'defaultType': 'swap'}
    })
    
    try:
        balance = exchange.fetch_balance()
        print("\n--- ¡CONEXIÓN ESTABLECIDA CON ÉXITO! ---")
        print(f"Total Equivalente USD: ${balance.get('total', {}).get('USDT', balance.get('total', {}).get('USD', 'N/A'))}")
    except Exception as e:
        print(f"\n[ERROR DE CONEXIÓN CON OKX]: {str(e)}")

