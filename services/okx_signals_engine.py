import os
import json
import random
from datetime import datetime
from license_db_manager import LicenseManager

class OKXSignalsEngine:
    def __init__(self):
        self.db = LicenseManager()
        self.pairs = ["BTC-USDT", "ETH-USDT", "SOL-USDT", "ZEEKR-USDT"]

    def generate_signal(self, license_key: str):
        is_valid, lic_data = self.db.verify_license(license_key)
        if not is_valid:
            return {"status": "ERROR", "message": "Licencia inválida o expirada. Suscríbete al Producto A."}

        # Simulación cuantitativa de mercado (Integrable con OKX REST API)
        pair = random.choice(self.pairs)
        action = random.choice(["BUY_LONG", "SELL_SHORT", "HOLD"])
        entry_price = round(random.uniform(100, 65000), 2)
        take_profit = round(entry_price * 1.04, 2)
        stop_loss = round(entry_price * 0.98, 2)

        signal = {
            "status": "SUCCESS",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "customer": lic_data.get("customer_name"),
            "signal": {
                "pair": pair,
                "action": action,
                "entry": entry_price,
                "take_profit": take_profit,
                "stop_loss": stop_loss,
                "leverage": "10x Cross"
            }
        }
        return signal
