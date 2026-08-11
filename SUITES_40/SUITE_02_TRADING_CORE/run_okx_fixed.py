# TOKYO OS (c) 2026 - TODOS LOS DERECHOS RESERVADOS - MARCA REGISTRADA
import os, json, hmac, hashlib, base64, time, requests

try:
    with open("okx_credentials.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    
    creds = config.get("credentials", {})
    api_key = creds.get("api_key")
    secret_key = creds.get("secret_key")

    base_url = "https://www.okx.com"
    endpoint = "/api/v5/account/balance"
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

    response = requests.get(base_url + endpoint, headers=headers, timeout=10)
    data = response.json()
    
    print("\n--- RESPUESTA OFICIAL DE LOS SERVIDORES DE OKX ---")
    print(f"Código de Estado HTTP: {response.status_code}")
    print(f"Código de Respuesta OKX (code): {data.get('code')}")
    print(f"Mensaje del Servidor (msg): {data.get('msg')}")
    
    if data.get("code") == "0":
        print("\n[ESTADO] ¡CONEXIÓN EXITOSA! Las llaves y la IP están perfectamente sincronizadas.")
        details = data.get("data", [])
        if details:
            print(f"Total de cuentas sincronizadas: {len(details)}")
    else:
        print("\n[ESTADO] LA CONEXIÓN FUE RECHAZADA POR OKX.")
        print("Revisa que la IP esté autorizada en tu panel de OKX o que los campos de las llaves no tengan espacios de más.")

except Exception as e:
    print(f"\n[ERROR DE EJECUCIÓN] {str(e)}")

