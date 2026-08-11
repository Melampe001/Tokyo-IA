# TOKYO OS (c) 2026 - TODOS LOS DERECHOS RESERVADOS - MARCA REGISTRADA
# ==============================================================================
# FLAGGSHIP APPS - OKX IP-SECURED CONNECTOR (2026)
# ==============================================================================
import os
import json
import hmac
import hashlib
import base64
import time
import requests

class OKXIPSecureConnector:
    def __init__(self, config_path):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        creds = self.config["credentials"]
        self.api_key = os.getenv("OKX_API_KEY", creds["api_key"])
        self.secret_key = os.getenv("OKX_SECRET_KEY", creds["secret_key"])
        # Passphrase omitida por seguridad de IP Whitelist
        self.base_url = "https://www.okx.com"

    def _sign(self, timestamp, method, request_path, body=""):
        message = timestamp + method.upper() + request_path + body
        mac = hmac.new(bytes(self.secret_key, encoding='utf-8'), bytes(message, encoding='utf-8'), digestmod=hashlib.sha256)
        return base64.b64encode(mac.digest()).decode('utf-8')

    def get_account_balance(self):
        endpoint = "/api/v5/account/balance"
        timestamp = str(int(time.time() * 1000))
        signature = self._sign(timestamp, "GET", endpoint)
        
        headers = {
            "OK-ACCESS-KEY": self.api_key,
            "OK-ACCESS-SIGN": signature,
            "OK-ACCESS-TIMESTAMP": timestamp,
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.get(self.base_url + endpoint, headers=headers)
            print("[OKX API] Conexión segura IP-Whitelist establecida.")
            return response.json()
        except Exception as e:
            print(f"[ERROR] Falló la conexión con OKX: {str(e)}")
            return None

if __name__ == "__main__":
    connector = OKXIPSecureConnector("okx_credentials.json")
    balance = connector.get_account_balance()
    if balance:
        print(json.dumps(balance, indent=4))

