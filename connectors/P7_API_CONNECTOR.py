import os
import time
import base64
import hmac
import hashlib
import json
import urllib.request
from datetime import datetime, timezone

class OKXIpAuthConnector:
    """
    Conector nativo OKX v5 optimizado para claves vinculadas por IP (sin Passphrase).
    """
    def __init__(self, api_key=None, secret_key=None):
        self.api_key = api_key or os.getenv("OKX_API_KEY", "")
        self.secret_key = secret_key or os.getenv("OKX_SECRET_KEY", "")
        self.base_url = "https://www.okx.com"

    def _get_timestamp(self):
        return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

    def _generate_signature(self, timestamp, method, request_path, body=""):
        message = f"{timestamp}{method}{request_path}{body}"
        mac = hmac.new(
            bytes(self.secret_key, encoding='utf-8'),
            bytes(message, encoding='utf-8'),
            digestmod=hashlib.sha256
        )
        return base64.b64encode(mac.digest()).decode('utf-8')

    def execute_request(self, method, request_path, params=None):
        if not self.api_key or not self.secret_key:
            print("[⚠️ OKX MOCK] Claves no presentes en entorno. Retornando ejecución simulada.")
            return {"code": "0", "msg": "SUCCESS_SIMULATED", "data": []}

        timestamp = self._get_timestamp()
        body_str = json.dumps(params) if params else ""
        signature = self._generate_signature(timestamp, method, request_path, body_str)

        headers = {
            "Content-Type": "application/json",
            "OK-ACCESS-KEY": self.api_key,
            "OK-ACCESS-SIGN": signature,
            "OK-ACCESS-TIMESTAMP": timestamp,
            "OK-ACCESS-PASSPHRASE": "", # Omitido/Vacio por vinculación explícita de IP
            "User-Agent": "TokyoApps-NulogicCore/1.0"
        }

        url = f"{self.base_url}{request_path}"
        try:
            req = urllib.request.Request(url, data=body_str.encode('utf-8') if body_str else None, headers=headers, method=method)
            with urllib.request.urlopen(req) as resp:
                res_data = json.loads(resp.read().decode('utf-8'))
                print(f"[✅ OKX API] Petición exitosa a {request_path}")
                return res_data
        except Exception as ex:
            print(f"[❌ OKX ERROR] Error de comunicación HTTP: {str(ex)}")
            return {"code": "500", "msg": str(ex)}

if __name__ == "__main__":
    connector = OKXIpAuthConnector()
    print("[✅] Conector OKX IP-Bound cargado correctamente.")
