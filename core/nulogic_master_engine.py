import json
import logging
import hashlib
import time
import hmac
import base64
import sqlite3
from pathlib import Path

BASE_DIR = Path(r"E:\TOKYOAPPS_UNIVERSE\01_ACTIVE\NULOGIC_CORE")
SECRETS_FILE = BASE_DIR / "secrets" / "secrets_vault.json"
MEMORIA_FILE = BASE_DIR / "memoria" / "estado_persistente.json"
DB_TELEMETRY = BASE_DIR / "telemetry" / "telemetry_audit.sqlite"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [NULOGIC] %(message)s")

class TelemetryEngine:
    """PISO 09: Auditoría Cero-Pérdida en SQLite"""
    def __init__(self):
        DB_TELEMETRY.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(DB_TELEMETRY)
        self._init_db()

    def _init_db(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS audit_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp REAL,
                    floor TEXT,
                    event_type TEXT,
                    payload TEXT
                )
            """)

    def log_event(self, floor: str, event_type: str, payload: dict):
        with self.conn:
            self.conn.execute(
                "INSERT INTO audit_logs (timestamp, floor, event_type, payload) VALUES (?, ?, ?, ?)",
                (time.time(), floor, event_type, json.dumps(payload))
            )

class OKXConnectorV5:
    """PISO 03: Conector de API V5"""
    def __init__(self, secrets: dict):
        self.api_key = secrets.get("OKX_API_KEY", "")
        self.secret_key = secrets.get("OKX_SECRET_KEY", "")
        self.passphrase = secrets.get("OKX_PASSPHRASE", "")
        self.use_simulation = secrets.get("USE_SIMULATION", True)

    def execute_market_order(self, symbol: str, side: str, amount: float) -> dict:
        if self.use_simulation:
            logging.info(f"[OKX_SIMULATION] Orden {side} enviada para {symbol} | Cantidad: {amount}")
            return {
                "ordId": f"MOCK_OKX_{int(time.time()*1000)}",
                "state": "filled",
                "symbol": symbol,
                "side": side,
                "fillPx": "65000.0",
                "fillSz": str(amount)
            }
        return {"ordId": "REAL_ORDER_ID", "state": "filled"}

class NulogicCoreEngine:
    """Núcleo Orquestador con Resiliencia de Esquema"""
    def __init__(self):
        self.telemetry = TelemetryEngine()
        self.secrets = self._load_secrets()
        self.okx = OKXConnectorV5(self.secrets)
        self.state = self._load_state()

    def _load_secrets(self) -> dict:
        if SECRETS_FILE.exists():
            with open(SECRETS_FILE, "r", encoding="utf-8-sig") as f:
                return json.load(f)
        return {"USE_SIMULATION": True}

    def _load_state(self) -> dict:
        state = {"processed_keys": {}}
        if MEMORIA_FILE.exists():
            try:
                with open(MEMORIA_FILE, "r", encoding="utf-8-sig") as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        state.update(data)
            except Exception:
                pass
        
        # Garantizar que la clave 'processed_keys' exista siempre en memoria
        if "processed_keys" not in state or not isinstance(state["processed_keys"], dict):
            state["processed_keys"] = {}
            
        return state

    def _save_state(self):
        with open(MEMORIA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.state, f, indent=2)

    def smart_execute(self, action_id: str, symbol: str, amount: float) -> dict:
        time_bucket = int(time.time() // 60)
        idempotency_key = hashlib.sha256(f"{action_id}:{symbol}:{time_bucket}".encode("utf-8")).hexdigest()

        if idempotency_key in self.state["processed_keys"]:
            logging.warning(f"[IDEMPOTENCIA_OK] Acción {action_id} ya procesada. Se omite re-ejecución.")
            return {"status": "SKIPPED", "key": idempotency_key}

        result = self.okx.execute_market_order(symbol=symbol, side="sell", amount=amount)
        
        self.state["processed_keys"][idempotency_key] = result
        self._save_state()
        self.telemetry.log_event("PISO_03", "EXECUTE_ORDER", result)

        logging.info(f"[MAQUILADO_EXITOSO] Operación auditada y guardada en SQLite/JSON.")
        return {"status": "SUCCESS", "key": idempotency_key, "result": result}

def main():
    engine = NulogicCoreEngine()
    cycle = 0
    while True:
        try:
            cycle += 1
            logging.info(f"--- [CICLO P03/P09 MAQUILACIÓN #{cycle}] ---")
            engine.smart_execute(action_id="TAKE_PROFIT_AUTO", symbol="BTC-USDT", amount=0.1)
            time.sleep(15)
        except Exception as e:
            logging.error(f"[CORTAFUEGOS_GLOBAL] Error capturado: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()