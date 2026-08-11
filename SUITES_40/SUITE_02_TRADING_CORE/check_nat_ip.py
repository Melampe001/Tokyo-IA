# TOKYO OS (c) 2026 - TODOS LOS DERECHOS RESERVADOS - MARCA REGISTRADA
import requests, time

try:
    print("[INFO] Probando consistencia de IP de salida en 3 saltos consecutivos...")
    ips = set()
    for i in range(3):
        res = requests.get("https://api.ipify.org", timeout=5)
        ip = res.text.strip()
        ips.add(ip)
        print(f" - Petición {i+1}: IP detectada = {ip}")
        time.sleep(1)
        
    if len(ips) == 1:
        print(f"\n[ESTABLE] Tu IP de salida es fija: {list(ips)[0]}")
        print("Si OKX sigue dando 50102 con IP fija, el problema es que la IP registrada")
        print("en el panel de OKX difiere por un dígito de esta IP de salida.")
    else:
        print(f"\n[ALERTA CRÍTICA] ¡Tu IP de salida está rotando! (IPs detectadas: {ips})")
        print("Tu proveedor de internet usa CGNAT o tienes una VPN/Proxy activa.")
        print("OKX bloqueará cualquier API Key con Whitelist estricta si la IP cambia.")

except Exception as e:
    print(f"[ERROR] {str(e)}")

