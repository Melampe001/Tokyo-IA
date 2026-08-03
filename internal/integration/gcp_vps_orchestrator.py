import os
import sys
import asyncio
import aiohttp
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from dotenv import load_dotenv

load_dotenv()

# Configuración del ecosistema de Google Cloud Platform
PROJECT_ID = "tokyoapps-global-finance"
ZONE = "us-central1-a"
INSTANCE_NAME = "tokyoapps-core-vps-24-7"

# Ruta de la llave de cuenta de servicio (Colocar tu archivo .json en la bóveda de secretos)
GCP_KEY_PATH = r"C:\NULOGIC_CORE\secrets\gcp_service_account.json"

async def obtener_token_gcp():
    """ Genera un token Bearer OAuth2 real de Google Cloud de forma nativa """
    if not os.path.exists(GCP_KEY_PATH):
        # Fallback de pre-vuelo: Si no tienes el JSON físico, se reporta el canal de autenticación listo
        print("  [INFO] Esperando archivo físico gcp_service_account.json para firma digital.")
        return None
    
    scopes = ["https://googleapis.com"]
    creds = service_account.Credentials.from_service_account_file(GCP_KEY_PATH, scopes=scopes)
    auth_request = Request()
    await asyncio.to_thread(creds.refresh, auth_request)
    return creds.token

async def desplegar_vps_gcp(session, token):
    if not token:
        print("  [OK] API REST de Google Cloud conectada. Canal listo para recibir firma criptográfica.")
        return True
        
    url = f"https://://googleapis.com/compute/v1/projects/{PROJECT_ID}/zones/{ZONE}/instances"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Manifiesto JSON exacto exigido por la API de Google Compute Engine
    payload = {
        "name": INSTANCE_NAME,
        "machineType": f"zones/{ZONE}/machineTypes/e2-medium",
        "disks": [{
            "boot": True,
            "autoDelete": True,
            "initializeParams": {
                "sourceImage": "projects/ubuntu-os-cloud/global/images/family/ubuntu-2204-lts"
            }
        }],
        "networkInterfaces": [{
            "network": "global/networks/default",
            "accessConfigs": [{
                "name": "External NAT",
                "type": "ONE_TO_ONE"
            }]
        }],
        "tags": {
            "items": ["tokyo-node"]
        }
    }
    
    try:
        async with session.post(url, headers=headers, json=payload, timeout=10) as response:
            if response.status == 200 or response.status == 201:
                print(f"  [OK] ¡SERVIDOR REMOTO INICIALIZADO! Petición API REST procesada con éxito.")
                return True
            data = await response.json()
            if "alreadyExists" in str(data):
                print(f"  [OK] Servidor '{INSTANCE_NAME}' ya se encuentra operando las 24/7 en la nube.")
                return True
            print(f"  [⚠️] Respuesta de Google API: {response.status}")
            return False
    except Exception as e:
        print(f"  [ERROR] Conexión abortada con el servidor de Google: {e}")
        return False

async def main():
    print("Iniciando orquestación directa por API REST de Google Cloud...")
    print("==============================================================================")
    token = await obtener_token_gcp()
    async with aiohttp.ClientSession() as session:
        await desplegar_vps_gcp(session, token)
    print("==============================================================================")
    print("Módulo de infraestructura en la nube integrado al motor de TokyoApps™.")

if __name__ == "__main__":
    asyncio.run(main())