import requests
from core_db import log_event
def check_github_status():
    try:
        res = requests.get("https://api.github.com/rate_limit", timeout=5).json()
        remaining = res["resources"]["core"]["remaining"]
        print(f"   🐙 [GITHUB] API Activa. Límite: {remaining}")
        log_event("GITHUB", "Conectado", "SUCCESS")
    except Exception as e: log_event("GITHUB", str(e), "ERROR")