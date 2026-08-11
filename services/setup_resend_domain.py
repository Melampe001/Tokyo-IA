# TOKYO OS (c) 2026 - TODOS LOS DERECHOS RESERVADOS - MARCA REGISTRADA
import os
import sys
import json
import urllib.request
import urllib.error

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

RESEND_API_KEY = os.getenv("RESEND_API_KEY", "")
TARGET_DOMAIN = os.getenv("OFFICIAL_DOMAIN", "tokyoapps.io")

def register_domain_in_resend():
    if not RESEND_API_KEY or len(RESEND_API_KEY) < 10:
        print("[❌ ERROR] RESEND_API_KEY no detectada en las variables de entorno.")
        return

    url = "https://api.resend.com/domains"
    payload = {
        "name": TARGET_DOMAIN,
        "region": "us-east-1"
    }
    headers = {
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json",
        "User-Agent": "TokyoApps-DomainManager/1.0"
    }

    print(f"[🌐] Solicitando registro DNS en Resend para el dominio: {TARGET_DOMAIN}...")

    try:
        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers, method="POST")
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            print(f"\n[✅ DOMINIO CREADO] ID: {res_data.get('id')}")
            print("==============================================================")
            print("📋 REGISTROS DNS A AGREGAR EN TU PROVEEDOR DE DOMINIO:")
            print("==============================================================")
            records = res_data.get("records", [])
            for r in records:
                print(f"Tipo: {r.get('record')} | Nombre: {r.get('name')} | Valor: {r.get('value')}")
            print("==============================================================")
    except urllib.error.HTTPError as e:
        err_body = e.read().decode('utf-8')
        if "already_exists" in err_body or "already been taken" in err_body:
            print(f"[ℹ️ INFO] El dominio '{TARGET_DOMAIN}' ya está dado de alta en tu panel de Resend.")
        else:
            print(f"[⚠️ ALERTA API] HTTP {e.code}: {err_body}")
    except Exception as ex:
        print(f"[❌ ERROR]: {str(ex)}")

if __name__ == "__main__":
    register_domain_in_resend()

