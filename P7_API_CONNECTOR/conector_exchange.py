# TOKYO OS (c) 2026 - TODOS LOS DERECHOS RESERVADOS - MARCA REGISTRADA
import os
import json

print("[*] Inicializando conector seguro para APIs del exchange...")

def verificar_credenciales():
    env_path = ".env"
    if not os.path.exists(env_path):
        # Si no existe el .env real, usamos la plantilla de referencia
        print("[AVISO] Archivo .env no detectado. Usando modo de simulación o plantilla.")
        return False
    print("[OK] Credenciales detectadas correctamente en entorno seguro.")
    return True

if __name__ == "__main__":
    verificar_credenciales()
