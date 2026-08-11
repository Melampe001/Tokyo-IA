# TOKYO OS (c) 2026 - TODOS LOS DERECHOS RESERVADOS - MARCA REGISTRADA
import os
import socket
import hmac
import base64
import json
import logging
import urllib.request
from datetime import datetime, timezone
from dotenv import load_dotenv

# Fuerza canal IPv4 a nivel de socket
_original_getaddrinfo = socket.getaddrinfo
def _forced_ipv4_getaddrinfo(*args, **kwargs):
    responses = _original_getaddrinfo(*args, **kwargs)
    return [resp for resp in responses if resp[0] == socket.AF_INET]
socket.getaddrinfo = _forced_ipv4_getaddrinfo

# Configuración de Logs en Vault
os.makedirs("vault_logs", exist_ok=True)
logging.basicConfig(
    filename="vault_logs/nulogic_execution.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

class NulogicCore:
    def __init__(self):
        load_dotenv(override=True)
        self.api_key = os.getenv("OKX_API_KEY", "").strip()
        self.secret_key = os.getenv("OKX_SECRET_KEY", "").strip()
        self.passphrase = os.getenv("OKX_PASSPHRASE", "").strip()
        self.base_url = "https://www.okx.com"

        if not all([self.api_key, self.secret_key, self.passphrase]):
            raise ValueError("Credenciales incompletas en .env (OKX_API_KEY, OKX_SECRET_KEY, OKX_PASSPHRASE)")

    def _signature(self, timestamp: str, method: str, path: str, body_str: str = "") -> str:
        message = f"{timestamp}{method}{path}{body_str}"
        mac = hmac.new(self.secret_key.encode('utf-8'), message.encode('utf-8'), digestmod='sha256')
        return base64.b64encode(mac.digest()).decode('utf-8')

    def request(self, method: str, path: str, params: dict = None, body: dict = None):
        if params:
            query = "?" + "&".join([f"{k}={v}" for k, v in params.items()])
            path += query

        timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        body_str = json.dumps(body, separators=(',', ':')) if body else ""
        sign = self._signature(timestamp, method.upper(), path, body_str)

        headers = {
            "OK-ACCESS-KEY": self.api_key,
            "OK-ACCESS-SIGN": sign,
            "OK-ACCESS-TIMESTAMP": timestamp,
            "OK-ACCESS-PASSPHRASE": self.passphrase,
            "Content-Type": "application/json",
            "User-Agent": "NULOGIC_CORE"
        }

        url = f"{self.base_url}{path}"
        data_bytes = body_str.encode('utf-8') if body_str else None
        req = urllib.request.Request(url, data=data_bytes, headers=headers, method=method.upper())

        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                res = json.loads(resp.read().decode('utf-8'))
                logging.info(f"{method} {path} -> Code: {res.get('code')}")
                return res
        except urllib.error.HTTPError as e:
            err_msg = e.read().decode('utf-8') if hasattr(e, 'read') else str(e)
            logging.error(f"HTTPError {e.code}: {err_msg}")
            return {"code": str(e.code), "msg": err_msg, "error": True}
        except Exception as e:
            logging.error(f"Error general: {str(e)}")
            return {"code": "-1", "msg": str(e), "error": True}

    def audit_account(self):
        print("\n--- AUDITORÍA DE CUENTA Y SALDOS ---")
        res = self.request("GET", "/api/v5/account/balance")
        if res.get("code") == "0":
            data = res.get("data", [{}])[0]
            print(f"Patrimonio Total: ${float(data.get('totalEq', '0')):.4f} USD")
            for item in data.get("details", []):
                eq = float(item.get("eq", "0"))
                if eq > 0:
                    print(f"  • Asset [{item.get('ccy')}]: Total={item.get('eq')} | Disponible={item.get('availBal')}")
        else:
            print(f"[ERROR BALANCE]: {res.get('msg')}")

    def execute_order(self, inst_id="BTC-USDT-SWAP", td_mode="cross", side="buy", pos_side="long", ord_type="market", sz="1"):
        print(f"\n--- EJECUCIÓN DIRECTA EN OKX: {inst_id} ---")
        payload = {
            "instId": inst_id,
            "tdMode": td_mode,
            "side": side,
            "posSide": pos_side,
            "ordType": ord_type,
            "sz": sz
        }
        res = self.request("POST", "/api/v5/trade/order", body=payload)
        
        code = res.get("code")
        if code == "0":
            order_data = res.get("data", [{}])[0]
            s_code = order_data.get("sCode")
            s_msg = order_data.get("sMsg")
            if s_code == "0":
                print(f"[ÉXITO] Orden Transmitida ID: {order_data.get('ordId')}")
            else:
                print(f"[RECHAZO MOTOR OKX] sCode {s_code}: {s_msg}")
        else:
            print(f"[FALLO API OKX] Code {code}: {res.get('msg')}")

if __name__ == "__main__":
    core = NulogicCore()
    core.audit_account()
    core.execute_order()
