import requests
from core_db import log_event
def fetch_okx_market():
    try:
        res = requests.get("https://www.okx.com/api/v5/market/ticker?instId=BTC-USDT", timeout=5).json()
        if res.get("code")=="0":
            price = float(res["data"][0]["last"])
            log_event("OKX", f"Precio: {price}", "SUCCESS")
            print(f"   📊 [OKX] BTC: ${price:,.2f}")
    except Exception as e: log_event("OKX", str(e), "ERROR")