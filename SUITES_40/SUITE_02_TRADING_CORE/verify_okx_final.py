import os, json, hmac, hashlib, base64, time, requests

try:
    with open("okx_credentials.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    
    creds = config.get("credentials", {})
    api_key = creds.get("api_key")
    secret_key = creds.get("secret_key")

    base_url = "https://www.okx.com"
    
    print("[INFO] Sincronizando con el reloj atómico de OKX...")
    time_res = requests.get(base_url + "/api/v5/public/time", timeout=5)
    server_time_data = time_res.json()
    
    if server_time_data.get("code") == "0":
        timestamp = str(server_time_data.get("data")[0].get("ts"))
    else:
        timestamp = str(int(time.time() * 1000))

    endpoint = "/api/v5/account/balance"
    message = timestamp + "GET" + endpoint
    
    mac = hmac.new(bytes(secret_key, encoding="utf-8"), bytes(message, encoding="utf-8"), digestmod=hashlib.sha256)
    signature = base64.b64encode(mac.digest()).decode("utf-8")

    headers = {
        "OK-ACCESS-KEY": api_key,
        "OK-ACCESS-SIGN": signature,
        "OK-ACCESS-TIMESTAMP": timestamp,
        "Content-Type": "application/json"
    }

    print("[INFO] Consultando balance con IP Megacable (200.56.180.63)...")
    response = requests.get(base_url + endpoint, headers=headers, timeout=10)
    data = response.json()
    
    print(f"\n--- RESPUESTA DE OKX ---")
    print(f"Código HTTP: {response.status_code}")
    print(f"Código OKX (code): {data.get('code')}")
    print(f"Mensaje: {data.get('msg')}")
    
    if data.get("code") == "0":
        print("\n[¡CONEXIÓN ESTABLECIDA CON ÉXITO ABSOLUTO!]")
        print("La autenticación HMAC y la Whitelist IP operan al 100%.")
        details = data.get("data", [])
        if details:
            for acc in details:
                print(f"Equivalente Total en Cuenta: ${acc.get('totalEq', '0')} USD")
    else:
        print("\n[AVISO TÉCNICO]")
        print("Si el código sigue siendo 50102, asegúrate de haber guardado cambios")
        print("en el panel de OKX y de que la API Key tenga activados los permisos de 'Trade'.")

except Exception as e:
    print(f"\n[ERROR] {str(e)}")
