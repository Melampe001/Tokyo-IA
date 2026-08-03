import os, json, hmac, hashlib, base64, time, requests

try:
    with open("okx_credentials.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    
    creds = config.get("credentials", {})
    api_key = creds.get("api_key")
    secret_key = creds.get("secret_key")

    base_url = "https://www.okx.com"
    
    # Obtenemos primero la hora exacta directamente del servidor de OKX para eliminar el desfase de Windows
    print("[INFO] Consultando sincronización de reloj con OKX...")
    time_res = requests.get(base_url + "/api/v5/public/time", timeout=5)
    server_time = int(time_res.json().get("data", [{}])[0].get("ts", time.time() * 1000))
    
    timestamp = str(server_time)
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

    response = requests.get(base_url + endpoint, headers=headers, timeout=10)
    data = response.json()
    
    print("\n--- NUEVA RESPUESTA OFICIAL DE OKX (SINCRONIZADA) ---")
    print(f"Código de Estado HTTP: {response.status_code}")
    print(f"Código de Respuesta OKX (code): {data.get('code')}")
    print(f"Mensaje del Servidor (msg): {data.get('msg')}")
    
    if data.get("code") == "0":
        print("\n[ESTADO] ¡CONEXIÓN EXITOSA Y VERIFICADA EN VIVO!")
        details = data.get("data", [])
        if details:
            print(f"Saldos sincronizados correctamente. Total de cuentas activas: {len(details)}")
    else:
        print("\n[ESTADO] LA API RESPONDIó PERO FUE RECHAZADA.")
        print("Causa probable: La IP desde donde ejecutas no coincide exactamente con la Whitelist configurada en OKX.")

except Exception as e:
    print(f"\n[ERROR DE EJECUCIÓN] {str(e)}")
