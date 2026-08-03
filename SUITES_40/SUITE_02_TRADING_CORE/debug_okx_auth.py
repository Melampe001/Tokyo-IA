import os, json, hmac, hashlib, base64, time, requests

try:
    with open("okx_credentials.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    
    creds = config.get("credentials", {})
    api_key = creds.get("api_key", "").strip()
    secret_key = creds.get("secret_key", "").strip()
    passphrase = creds.get("passphrase")

    print(f"[VERIFICACIÓN LOCAL] API Key cargada (Longitud: {len(api_key)}, Mask: {api_key[:5]}...)")
    print(f"[VERIFICACIÓN LOCAL] Secret Key cargada (Longitud: {len(secret_key)})")

    if not api_key or api_key == "TU_API_KEY_AQUI":
        print("[ERROR] La API Key sigue teniendo el valor por defecto o está vacía.")
        exit(1)

    base_url = "https://www.okx.com"
    endpoint = "/api/v5/public/time"  # Probamos primero con endpoint público para descartar permisos de cuenta
    
    timestamp = str(int(time.time() * 1000))
    message = timestamp + "GET" + endpoint
    
    mac = hmac.new(bytes(secret_key, encoding="utf-8"), bytes(message, encoding="utf-8"), digestmod=hashlib.sha256)
    signature = base64.b64encode(mac.digest()).decode("utf-8")

    headers = {
        "OK-ACCESS-KEY": api_key,
        "OK-ACCESS-SIGN": signature,
        "OK-ACCESS-TIMESTAMP": timestamp,
        "Content-Type": "application/json"
    }

    print("\n[INFO] Probando firma en endpoint público de OKX...")
    response = requests.get(base_url + endpoint, headers=headers, timeout=10)
    print(f"Respuesta HTTP (endpoint público): {response.status_code}")
    print(f"Contenido: {response.text}")

except Exception as e:
    print(f"\n[EXCEPCIÓN] {str(e)}")
