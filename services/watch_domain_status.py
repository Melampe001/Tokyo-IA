import os
import sys
import time
import json
import urllib.request
import winsound

RESEND_API_KEY = os.getenv("RESEND_API_KEY", "")
DOMAIN_ID = "c08d3cb7-705d-455f-addd-251a79fcf005"
DOMAIN_NAME = "tokyoapps.com"
INTERVAL_SECONDS = 30

def check_and_verify():
    if not RESEND_API_KEY:
        print("[❌ ERROR] RESEND_API_KEY no detectada en el entorno.")
        return False, "NO_API_KEY"

    headers = {
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json",
        "User-Agent": "TokyoApps-DomainWatcher/1.0"
    }

    # Force re-verification scan with empty JSON payload (Fix HTTP 400)
    try:
        verify_url = f"https://api.resend.com/domains/{DOMAIN_ID}/verify"
        empty_data = json.dumps({}).encode('utf-8')
        req_verify = urllib.request.Request(verify_url, data=empty_data, headers=headers, method="POST")
        urllib.request.urlopen(req_verify)
    except Exception:
        pass

    # Read domain status
    get_url = f"https://api.resend.com/domains/{DOMAIN_ID}"
    try:
        req_get = urllib.request.Request(get_url, headers=headers, method="GET")
        with urllib.request.urlopen(req_get) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            status = data.get("status", "unknown")
            return True, status
    except Exception as ex:
        return False, str(ex)

def start_watching():
    print(f"==============================================================")
    print(f"[🔍 MONITOR ACTIVADO] Monitoreando '{DOMAIN_NAME}' cada {INTERVAL_SECONDS}s")
    print(f"==============================================================")

    attempt = 1
    while True:
        timestamp = time.strftime("%H:%M:%S")
        success, status = check_and_verify()

        if success:
            if status == "verified":
                print(f"\n[{timestamp}] 🎉 ¡ÉXITO! El dominio '{DOMAIN_NAME}' ha sido VERIFICADO.")
                for _ in range(3):
                    winsound.Beep(1000, 300)
                    winsound.Beep(1500, 400)
                print("[🚀] NULOGIC_CORE listo para enviar correos reales desde onboarding@tokyoapps.com")
                break
            else:
                print(f"[{timestamp}] Intento #{attempt}: Estado = '{status}' | Reintentando en {INTERVAL_SECONDS}s...")
        else:
            print(f"[{timestamp}] Intento #{attempt}: Error de consulta ({status}) | Reintentando...")

        attempt += 1
        time.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    start_watching()
