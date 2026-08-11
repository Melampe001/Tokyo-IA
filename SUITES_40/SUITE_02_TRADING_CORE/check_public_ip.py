# TOKYO OS (c) 2026 - TODOS LOS DERECHOS RESERVADOS - MARCA REGISTRADA
import requests

try:
    print("[INFO] Consultando IP pública actual...")
    response = requests.get("https://api.ipify.org?format=json", timeout=5)
    ip_data = response.json()
    public_ip = ip_data.get("ip")
    
    print(f"\n==================================================")
    print(f" TU IP PÚBLICA ACTUAL ES: {public_ip}")
    print(f"==================================================")
    print("\n[INSTRUCCIÓN CRÍTICA DE SEGURIDAD]:")
    print("1. Entra a tu cuenta de OKX -> API -> Gestionar API Keys.")
    print("2. Asegúrate de que esta dirección IP (" + public_ip + ") esté")
    print("   exactamente registrada en la 'IP Whitelist' (Lista blanca de IPs).")
    print("3. Si estás usando una VPN o tu proveedor te cambia la IP dinámica,")
    print("   la conexión será bloqueada por OKX automáticamente.")
    
except Exception as e:
    print(f"[ERROR] No se pudo obtener la IP pública: {str(e)}")

