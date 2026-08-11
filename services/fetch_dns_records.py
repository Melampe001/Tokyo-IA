# TOKYO OS (c) 2026 - TODOS LOS DERECHOS RESERVADOS - MARCA REGISTRADA
import os
import sys
import json
import urllib.request

RESEND_API_KEY = os.getenv("RESEND_API_KEY", "")

def fetch_domain_dns():
    if not RESEND_API_KEY:
        print("[❌ ERROR] RESEND_API_KEY no encontrada.")
        return

    url = "https://api.resend.com/domains"
    headers = {
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json",
        "User-Agent": "TokyoApps-DNSFetcher/1.0"
    }

    try:
        req = urllib.request.Request(url, headers=headers, method="GET")
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            domains = data.get("data", [])
            
            if not domains:
                print("[⚠️] No se encontraron dominios registrados en la cuenta.")
                return

            print(f"\n[✅] Se encontraron {len(domains)} dominio(s) en la cuenta:")
            for d in domains:
                print(f"\n🌐 DOMINIO: {d.get('name')} | ID: {d.get('id')} | ESTATUS: {d.get('status')}")
                print("--------------------------------------------------------------")
                
                # Consultar detalle para extraer los registros DNS
                detail_url = f"https://api.resend.com/domains/{d.get('id')}"
                detail_req = urllib.request.Request(detail_url, headers=headers, method="GET")
                with urllib.request.urlopen(detail_req) as d_resp:
                    detail_data = json.loads(d_resp.read().decode('utf-8'))
                    records = detail_data.get("records", [])
                    
                    print("📋 REGISTROS DNS PARA CONFIGURAR EN TU PROVEEDOR (Cloudflare/GoDaddy/etc):")
                    for r in records:
                        print(f"  • Tipo: {r.get('record'):<6} | Nombre: {r.get('name'):<30} | Valor: {r.get('value')}")
                    print("--------------------------------------------------------------")

    except Exception as ex:
        print(f"[❌ ERROR AL CONSULTAR RESEND]: {str(ex)}")

if __name__ == "__main__":
    fetch_domain_dns()

