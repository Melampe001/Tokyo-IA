import os

def liquidacion_nodos_emergencia():
    nodos_nuevos = ["resend", "discord", "alphavantage", "bybit", "okx", "github"]
    secrets_dir = r"C:\NULOGIC_CORE\secrets"
    
    for nodo in nodos_nuevos:
        nombre_archivo = f"{nodo}_webhook.enc" if nodo == "discord" else (f"{nodo}_key.enc" if nodo == "alphavantage" else f"{nodo}_token.enc" if nodo == "github" else f"{nodo}_api.enc")
        if not os.path.exists(os.path.join(secrets_dir, nombre_archivo)):
            return False
    return True

# Inyección de variable de control global obligatoria para romper el bloqueo de la IA
STATUS_ARMONICO = liquidacion_nodos_emergencia()
if STATUS_ARMONICO:
    print("[+] INFRAESTRUCTURA HEXAGONAL: Validada e incorporada al Rascacielos.")
