import os, json, hmac, hashlib, base64, datetime, requests, socket

# Forzar resolución DNS a IPv4 (A record only) para evitar que requests tome IPv6 de Megacable
old_getaddrinfo = socket.getaddrinfo
def new_getaddrinfo(*args, **kwargs):
    responses = old_getaddrinfo(*args, **kwargs)
    return [r for r in responses if r[0] == socket.AF_INET]
socket.getaddrinfo = new_getaddrinfo

try:
    credential_paths = [
        "okx_credentials.json",
        "../okx_credentials.json",
        r"E:\TOKYOAPPS_UNIVERSE\01_ACTIVE\NULOGIC_CORE\SUITES_40\SUITE_02_TRADING_CORE\okx_credentials.json"
    ]

    config = None
    for path in credential_paths:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                config = json.load(f)
            break

    if not config:
        raise FileNotFoundError("[ERROR CRÍTICO] No se localizó 'okx_credentials.json'.")

    creds = config.get("credentials", {})
    api_key = creds.get("api_key", "").strip()
    secret_key = creds.get("secret_key", "").strip()
    passphrase = creds.get("passphrase", "").strip()

    base_url = "https://www.okx.com"
    endpoint = "/api/v5/account/balance"

    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")
    print(f"[✅] SSoT OKX Timestamp ISO: {timestamp}")

    message = timestamp + "GET" + endpoint
    mac = hmac.new(bytes(secret_key, encoding="utf-8"), bytes(message, encoding="utf-8"), digestmod=hashlib.sha256)
    signature = base64.b64encode(mac.digest()).decode("utf-8")

    headers = {
        "OK-ACCESS-KEY": api_key,
        "OK-ACCESS-SIGN": signature,
        "OK-ACCESS-TIMESTAMP": timestamp,
        "OK-ACCESS-PASSPHRASE": passphrase,
        "Content-Type": "application/json"
    }

    print("[INFO] Enviando petición privada a OKX forzando salida IPv4 (200.56.180.63)...")
    response = requests.get(base_url + endpoint, headers=headers, timeout=10)
    data = response.json()
    
    print(f"\n--- RESPUESTA OFICIAL DE OKX ---")
    print(f"Código HTTP: {response.status_code}")
    print(f"Código OKX (code): {data.get('code')}")
    print(f"Mensaje: {data.get('msg')}")
    
    if data.get("code") == "0":
        print("\n[¡CONEXIÓN Y AUTORIZACIÓN EXITOSAS EN VIVO!]")
        details = data.get("data", [])
        if details:
            for acc in details:
                print(f"Equivalente Total en Cuenta: ${acc.get('totalEq', '0')} USD")
    else:
        print(f"\n[AVISO TÉCNICO] Código devuelto: {data.get('code')} - {data.get('msg')}")

except Exception as e:
    print(f"\n[ERROR CRÍTICO] {str(e)}")
