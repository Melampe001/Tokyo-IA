import os, json, hmac, hashlib, base64, time, requests

try:
    with open("okx_credentials.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    
    creds = config.get("credentials", {})
    api_key = creds.get("api_key", "").strip()
    secret_key = creds.get("secret_key", "").strip()
    passphrase = creds.get("passphrase", "").strip()

    base_url = "https://www.okx.com"
    endpoint = "/api/v5/account/balance"
    
    # 1. Sincronización exacta de marca de tiempo con el servidor de OKX
    time_res = requests.get(base_url + "/api/v5/public/time", timeout=5)
    server_time = time_res.json().get("data", [{}])[0].get("ts", int(time.time() * 1000))
    timestamp = str(server_time)
    
    # 2. Generación de firma criptográfica HMAC-SHA256
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

    print("[INFO] Consultando balance general en vivo con la IP autorizada...")
    response = requests.get(base_url + endpoint, headers=headers, timeout=10)
    data = response.json()
    
    print(f"\n--- RESPUESTA OFICIAL DE OKX ---")
    print(f"Código HTTP: {response.status_code}")
    print(f"Código de Respuesta (code): {data.get('code')}")
    print(f"Mensaje del Servidor (msg): {data.get('msg')}")
    
    if data.get("code") == "0":
        print("\n[¡ÉXITO TOTAL!] ¡Conexión establecida y autorizada!")
        details = data.get("data", [])
        if details:
            for acc in details:
                print(f"Equivalente Total en Cuenta: ${acc.get('totalEq', '0')} USD")
                balances = acc.get("details", [])
                for asset in balances:
                    if float(asset.get("cashBal", 0)) > 0:
                        print(f" -> Activo: {asset.get('ccy')} | Saldo: {asset.get('cashBal')}")
    else:
        print(f"\n[AVISO] OKX respondió con código: {data.get('code')} -> {data.get('msg')}")

except Exception as e:
    print(f"\n[ERROR DE EJECUCIÓN] {str(e)}")
