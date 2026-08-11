# TOKYO OS (c) 2026 - TODOS LOS DERECHOS RESERVADOS - MARCA REGISTRADA
import os, json, hmac, hashlib, base64, time, requests

try:
    with open("okx_credentials.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    
    creds = config.get("credentials", {})
    api_key = creds.get("api_key")
    secret_key = creds.get("secret_key")

    base_url = "https://www.okx.com"
    
    # 1. Obtener timestamp directo del servidor de OKX (evita desfases de Windows)
    print("[INFO] Sincronizando marca de tiempo con el servidor de OKX...")
    time_res = requests.get(base_url + "/api/v5/public/time", timeout=5)
    server_time_data = time_res.json()
    
    if server_time_data.get("code") == "0":
        timestamp = server_time_data.get("data")[0].get("ts")
    else:
        timestamp = str(int(time.time() * 1000))

    endpoint = "/api/v5/account/balance"
    message = str(timestamp) + "GET" + endpoint
    
    mac = hmac.new(bytes(secret_key, encoding="utf-8"), bytes(message, encoding="utf-8"), digestmod=hashlib.sha256)
    signature = base64.b64encode(mac.digest()).decode("utf-8")

    headers = {
        "OK-ACCESS-KEY": api_key,
        "OK-ACCESS-SIGN": signature,
        "OK-ACCESS-TIMESTAMP": str(timestamp),
        "Content-Type": "application/json"
    }

    print("[INFO] Ejecutando consulta de balance con timestamp sincronizado...")
    response = requests.get(base_url + endpoint, headers=headers, timeout=10)
    data = response.json()
    
    if data.get("code") == "0":
        print("\n[ÉXITO TOTAL] ¡Conexión establecida y autorizada!")
        print(f"Código HTTP: {response.status_code}")
        
        details = data.get("data", [])
        if details:
            print("\n--- RESUMEN DE ACTIVOS DE LA CUENTA ---")
            for acc in details:
                total_eq = acc.get("totalEq", "0")
                print(f"Equivalente Total en USD: ${total_eq}")
                balances = acc.get("details", [])
                for asset in balances:
                    if float(asset.get("cashBal", 0)) > 0:
                        print(f" - {asset.get('ccy')}: {asset.get('cashBal')}")
    else:
        print(f"\n[ERROR] OKX respondió con código {data.get('code')}: {data.get('msg')}")

except Exception as e:
    print(f"\n[ERROR CRÍTICO] {str(e)}")

