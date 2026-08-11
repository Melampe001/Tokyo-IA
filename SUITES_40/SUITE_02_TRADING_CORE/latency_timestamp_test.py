# TOKYO OS (c) 2026 - TODOS LOS DERECHOS RESERVADOS - MARCA REGISTRADA
import os, json, hmac, hashlib, base64, time, requests

try:
    with open("okx_credentials.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    
    creds = config.get("credentials", {})
    api_key = creds.get("api_key")
    secret_key = creds.get("secret_key")

    base_url = "https://www.okx.com"
    
    # Medir el tiempo de ida y vuelta (RTT) y la diferencia con el servidor OKX
    local_before = int(time.time() * 1000)
    time_res = requests.get(base_url + "/api/v5/public/time", timeout=5)
    local_after = int(time.time() * 1000)
    
    rtt = local_after - local_before
    server_time_data = time_res.json()
    
    if server_time_data.get("code") == "0":
        server_ts = int(server_time_data.get("data")[0].get("ts"))
        # Offset: Ajustamos sumando la mitad del RTT para compensar el viaje de la red
        estimated_current_server_ts = server_ts + (rtt // 2)
        print(f"[INFO] RTT de red: {rtt} ms | Servidor OKX TS: {server_ts}")
        timestamp = str(estimated_current_server_ts)
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

    print(f"[INFO] Enviando petición con timestamp ajustado: {timestamp}")
    response = requests.get(base_url + endpoint, headers=headers, timeout=10)
    data = response.json()
    
    print("\n--- RESULTADO DE LA PRUEBA CON COMPENSACIÓN DE RED ---")
    print(f"Código HTTP: {response.status_code}")
    print(f"Código OKX (code): {data.get('code')}")
    print(f"Mensaje: {data.get('msg')}")
    
    if data.get("code") == "0":
        print("\n[¡ÉXITO!] ¡La firma y el timestamp fueron aceptados por OKX!")
        details = data.get("data", [])
        if details:
            print(f"Cuentas sincronizadas con éxito. Total: {len(details)}")
    else:
        print("\n[DIAGNÓSTICO ADICIONAL]:")
        print("Si el timestamp ya está perfectamente sincronizado y sigue dando 50102,")
        print("el 99% de las veces significa que la dirección IP desde donde sales a internet")
        print("no coincide con la registrada en la API Key (por ejemplo, tu proveedor usa CGNAT")
        print("o tienes una VPN/Proxy activa que cambia tu IP de salida en cada petición).")

except Exception as e:
    print(f"\n[ERROR] {str(e)}")

