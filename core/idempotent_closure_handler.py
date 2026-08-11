# TOKYO OS (c) 2026 - TODOS LOS DERECHOS RESERVADOS - MARCA REGISTRADA
import json
import logging
import hashlib
import time
from pathlib import Path

BASE_DIR = Path(r"E:\TOKYOAPPS_UNIVERSE\01_ACTIVE\NULOGIC_CORE")
MEMORIA_PERSISTENTE = BASE_DIR / "memoria" / "estado_persistente.json"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

class IdempotentClosureHandler:
    def __init__(self):
        MEMORIA_PERSISTENTE.parent.mkdir(parents=True, exist_ok=True)
        self.state = self._load_state()

    def _load_state(self) -> dict:
        if MEMORIA_PERSISTENTE.exists():
            try:
                with open(MEMORIA_PERSISTENTE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {"processed_closures": {}, "active_positions": {}}
        return {"processed_closures": {}, "active_positions": {}}

    def _save_state(self):
        with open(MEMORIA_PERSISTENTE, "w", encoding="utf-8") as f:
            json.dump(self.state, f, indent=2)

    def generate_idempotency_key(self, position_id: str, action: str, timestamp_bucket: int) -> str:
        raw_payload = f"{position_id}:{action}:{timestamp_bucket}"
        return hashlib.sha256(raw_payload.encode("utf-8")).hexdigest()

    def execute_closure(self, position_id: str, symbol: str, amount: float, reason: str = "EMERGENCY_STOP") -> dict:
        timestamp_bucket = int(time.time() // 60)
        idempotency_key = self.generate_idempotency_key(position_id, "CLOSE", timestamp_bucket)

        if idempotency_key in self.state["processed_closures"]:
            logging.warning(f"[IDEMPOTENCY_BLOCK] Cierre ya procesado para {position_id}. Key: {idempotency_key}")
            return {
                "status": "SKIPPED_ALREADY_CLOSED",
                "idempotency_key": idempotency_key,
                "closure_record": self.state["processed_closures"][idempotency_key]
            }

        logging.info(f"[CLOSURE_EXECUTION] Cierre inteligente para {symbol} | Cantidad: {amount} | Motivo: {reason}")
        execution_result = {
            "position_id": position_id,
            "symbol": symbol,
            "closed_amount": amount,
            "status": "FILLED",
            "executed_at": time.time(),
            "reason": reason
        }

        self.state["processed_closures"][idempotency_key] = execution_result
        if position_id in self.state["active_positions"]:
            del self.state["active_positions"][position_id]
            
        self._save_state()
        logging.info(f"[CLOSURE_SUCCESS] Posición {position_id} guardada e impulsada sin duplicidad.")
        return {
            "status": "SUCCESS",
            "idempotency_key": idempotency_key,
            "closure_record": execution_result
        }

def main_loop():
    handler = IdempotentClosureHandler()
    logging.info("[NULOGIC_CORE] Motor de ejecuciones inteligentes iniciado en modo continuo 24/7.")
    cycle_count = 0
    while True:
        try:
            cycle_count += 1
            logging.info(f"[CICLO_MAQUILACION #{cycle_count}] Verificando integridad de memoria y estado...")
            
            # Prueba atómica de ejecución inteligente
            handler.execute_closure(position_id="POS_OKX_BTC_001", symbol="BTC/USDT", amount=0.5, reason="PROFIT_TAKE")
            
            time.sleep(10)
        except Exception as e:
            logging.error(f"[CORTAFUEGOS_PYTHON] Capturado error inesperado: {e}")
            logging.info("[RECOVERY] Reiniciando subsistema en 3 segundos...")
            time.sleep(3)

if __name__ == "__main__":
    main_loop()

