# TOKYO OS (c) 2026 - TODOS LOS DERECHOS RESERVADOS - MARCA REGISTRADA
import os, json

credential_paths = [
    "okx_credentials.json",
    "../okx_credentials.json",
    r"E:\TOKYOAPPS_UNIVERSE\01_ACTIVE\NULOGIC_CORE\SUITES_40\SUITE_02_TRADING_CORE\okx_credentials.json"
]

config = None
found_path = None
for path in credential_paths:
    if os.path.exists(path):
        found_path = path
        with open(path, "r", encoding="utf-8") as f:
            config = json.load(f)
        break

if not config:
    print("[ERROR CRÍTICO] No se encontró el archivo 'okx_credentials.json' en ninguna ruta.")
    exit(1)

print(f"[INFO] Archivo localizado en: {found_path}")
print(f"Estructura raíz de las llaves: {list(config.keys())}")

# Evaluar si las credenciales están anidadas bajo 'credentials' o en la raíz
creds = config.get("credentials", config)

api_key = creds.get("api_key", creds.get("apiKey", ""))
secret_key = creds.get("secret_key", creds.get("secret", ""))
passphrase = creds.get("passphrase", creds.get("password", ""))

print(f" - API Key presente   : {'SÍ (Longitud: ' + str(len(api_key)) + ')' if api_key else 'NO ❌'}")
print(f" - Secret Key presente: {'SÍ (Longitud: ' + str(len(secret_key)) + ')' if secret_key else 'NO ❌'}")
print(f" - Passphrase presente: {'SÍ (Longitud: ' + str(len(passphrase)) + ')' if passphrase else 'NO ❌'}")

if not api_key or not secret_key or not passphrase:
    print("\n[⚠️ ALERTA] Faltan componentes en el token de acceso. Revise su JSON.")
else:
    print("\n[✅ ÉXITO] El token de acceso posee todos los componentes estructurales requeridos.")

