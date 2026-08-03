# ==============================================================================
# FLAGGSHIP APPS - OKX LIVE CONNECTION VERIFIER (2026)
# ==============================================================================
import os
import json
import hmac
import hashlib
import base64
import time
import requests

def test_live_connection():
    config_path = "okx_credentials.json"
    if not os.path.exists(config_path):
        print(f"[ERROR] No se encuentra el archivo {config_path}")
        return

    with open(config_path, 'r') as f:
        config = json.load(f)

    if config.get("simulation") is not False:
        print("[ALERTA] El archivo indica modo simulación. Debe estar en false para operar en real.")
        return

    creds = config.get("credentials", {})
    api_key = creds.get("api_key")
    secret_key = creds.get("secret_key")

    if not api_key or "YOUR_" in api_key or not secret_key or "YOUR_" in secret_key:
        print("[ERROR] Aún tienes las llaves por defecto en 'okx_credentials.json'. Ingresa tus llaves reales.")
        return

    base_url = "https://www.okx.com"
    endpoint = "/api/v5/account/balance"
    timestamp = str(int(time.time() * 1000))
    
    message = timestamp + "GET" + endpoint
    mac = hmac.new(bytes(secret_key, encoding='utf-8'), bytes(message, encoding='utf-8'), digestmod=hashlib.sha256)
    signature = base64.b64encode(mac.digest()).decode('utf-8')

    headers = {
        "OK-ACCESS-KEY": api_key,
        "OK-ACCESS-SIGN": signature,
        "OK-ACCESS-TIMESTAMP": timestamp,
        "Content-Type": "application/json"
    }

    print("[INFO] Consultando balance y estado de cuenta en vivo en OKX...")
    try:
        response = requests.get(base_url + endpoint, headers=headers, timeout=10)
        data = response.json()
        
        if data.get("code") == "0":
            print("\n[ÉXITO ABSOLUTO] ¡Conexión en vivo establecida correctamente con OKX!")
            print("[ESTADO] Las llaves son válidas, la IP está autorizada y el canal de trading está abierto.")
            balances = data.get("data", [])
            for b in balances:
                print(f" - Monedas con balance en cuenta: {len(b.get('details', []))}")
        else:
            print(f"\n[RECHAZADO] OKX respondió con código de error: {data.get('code')}")
            print(f"Motivo: {data.get('msg')}")
            print("Verifica que tus llaves sean correctas y que tu IP esté en la lista blanca de OKX.")
            
    except Exception as e:
        print(f"[ERROR DE CONEXIÓN] {str(e)}")

if __name__ == "__main__":
    test_live_connection()
