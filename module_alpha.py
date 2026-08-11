import requests
from core_db import log_event
def fetch_alpha_macro():
    try:
        res = requests.get("https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=IBM&apikey=demo", timeout=5).json()
        price = res["Global Quote"].get("05. price", "N/A")
        log_event("ALPHA", f"Precio: {price}", "SUCCESS")
        print(f"   📈 [ALPHA] IBM: ${price}")
    except Exception as e: log_event("ALPHA", str(e), "ERROR")