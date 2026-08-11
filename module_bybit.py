# TOKYO OS (c) 2026 - TODOS LOS DERECHOS RESERVADOS - MARCA REGISTRADA
import requests
from core_db import log_event
def fetch_bybit_liquidity():
    try:
        res = requests.get("https://api.bybit.com/v5/market/tickers?category=spot&symbol=BTCUSDT", timeout=5).json()
        if res.get("retCode")==0:
            price = float(res["result"]["list"][0]["lastPrice"])
            log_event("BYBIT", f"Precio: {price}", "SUCCESS")
            print(f"   🌊 [BYBIT] BTC: ${price:,.2f}")
    except Exception as e: log_event("BYBIT", str(e), "ERROR")
