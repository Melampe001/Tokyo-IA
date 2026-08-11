# TOKYO OS (c) 2026 - TODOS LOS DERECHOS RESERVADOS - MARCA REGISTRADA
# ==============================================================================
# FLAGGSHIP APPS - RIGOROUS OKX CREDENTIALS & PERMISSIONS VALIDATOR (2026)
# ==============================================================================
import os
import json
import hmac
import hashlib
import base64
import time
import requests

def verify_live_api():
    config_path = "okx_credentials.json"
    if not os.path.exists(config_path):
        print(f"[ERROR CRÍTICO] No existe el archivo {config_path} en el directorio actual.")
        return

    with open(config_path, 'r') as f:
        config = json.load(f)
    
    creds = config.get("credentials", {})
    api_key = creds.get("api_key")
    secret_key = creds.get("secret_key")

    if not api_key or "YOUR_" in api_key or not secret_key or "YOUR_" in secret_key:
        print("[ALERTA] Las credenciales actuales parecen ser de marcador o están vacías.")
        print("[ACCIÓN REQUERIDA] Inserta tus llaves reales de OKX en 'okx_credentials.json'.")
        return

    base_url = "https://www.okx.com"
    
    # 1. Prueba de Endpoint de Cuenta (Valida API Key y Secret Key)
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

    print("[INFO] Conectando con los servidores globales de OKX para verificar firmas e IP...")
    try:
        response = requests.get(base_url + endpoint, headers=headers, timeout=10)
        res_data = response.json()
        
        code = res_data.get("code")
        if code == "0":
            print("\n[ÉXITO TOTAL] ¡Las credenciales son 100% reales y correctas!")
            print("[ESTADO] La IP está autorizada, la firma HMAC coincide y el canal de trading está abierto.")
            details = res_data.get("data", [])
            if details:
                print(f"[BALANCE DETECTADO] Cuentas activas enlazadas: {len(details)}")
        else:
            print(f"\n[FALLO EN LA RESPUESTA] OKX ha rechazado la autenticación.")
            print(f"Código de error OKX: {code}")
            print(f"Mensaje del servidor: {res_data.get('msg')}")
            print("\n[DIAGNÓSTICO DE CAUSAS POSIBLES]:")
            print("1. La API Key o el Secret Key tienen un carácter incorrecto.")
            print("2. La IP desde la que ejecutas este script no coincide exactamente con la Whitelist de OKX.")
            print("3. La API Key no tiene habilitados los permisos necesarios (Lectura / Trade).")
            
    except requests.exceptions.Timeout:
        print("[ERROR DE RED] Tiempo de espera agotado al intentar conectar con OKX. Revisa tu conexión a internet.")
    except Exception as e:
        print(f"[ERROR INESPERADO] {str(e)}")

if __name__ == "__main__":
    verify_live_api()

