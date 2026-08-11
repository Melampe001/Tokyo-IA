# TOKYO OS (c) 2026 - TODOS LOS DERECHOS RESERVADOS - MARCA REGISTRADA
import requests
from core_db import log_event

def fetch_okx_market():
    try:
        res = requests.get("https://www.okx.com/api/v5/market/ticker?instId=BTC-USDT", timeout=5).json()
        if res.get("code") == "0":
            price = float(res["data"][0]["last"])
            log_event("OKX", f"BTC: {price}", "SUCCESS")
            return price
    except Exception as e:
        log_event("OKX", str(e), "ERROR")
    return None

def fetch_bybit_liquidity():
    try:
        res = requests.get("https://api.bybit.com/v5/market/tickers?category=spot&symbol=BTCUSDT", timeout=5).json()
        if res.get("retCode") == 0:
            price = float(res["result"]["list"][0]["lastPrice"])
            log_event("BYBIT", f"BTC: {price}", "SUCCESS")
            return price
    except Exception as e:
        log_event("BYBIT", str(e), "ERROR")
    return None

def check_github_status():
    try:
        headers = {"Accept": "vnd.github+json", "User-Agent": "NulogicSovereign/3.0"}
        res = requests.get("https://api.github.com/meta", headers=headers, timeout=5)
        if res.status_code == 200:
            log_event("GITHUB", "Canal seguro activo", "SUCCESS")
            return True
    except Exception as e:
        log_event("GITHUB", f"Watchdog red: {e}", "WARNING")
    return False
