# TOKYO OS (c) 2026 - TODOS LOS DERECHOS RESERVADOS - MARCA REGISTRADA
import elara
import json
from fastapi import FastAPI, Header, HTTPException
from datetime import datetime

app = FastAPI(title="NEXUS-1 Industrial API Gateway - TokyoApps", version="1.0.0")

# Bóveda Soberana (Piso 7) para control de créditos y balances
db = elara.exe_secure("sovereign_vault.db", commitdb=True, key_path="vault_master.key")

COSTO_POR_LLAMADA = 0.05  # USD por cada ejecución de IA o procesamiento

@app.post("/nexus/v1/execute")
async def ejecutar_servicio_nexus(prompt: str, x_api_key: str = Header(...)):
    """
    Endpoint B2B Industrial de NEXUS-1:
    Verifica la API Key, descuenta el saldo por llamada en tiempo real y registra la transacción.
    """
    # 1. Validar existencia de la API Key en la base de datos segura
    user_key_path = f"api_keys_{x_api_key}"
    user_data = db.get(user_key_path)
    
    if not user_data:
        raise HTTPException(status_code=401, detail="API Key inválida o no registrada en NEXUS-1.")
    
    saldo_usuario = user_data.get("credits_balance", 0.0)
    
    # 2. Verificar Rate Limiting / Créditos suficientes
    if saldo_usuario < COSTO_POR_LLAMADA:
        raise HTTPException(status_code=403, detail="Créditos insuficientes. Recargue saldo en la Bóveda.")
    
    # 3. Descontar costo de la llamada
    nuevo_saldo = round(saldo_usuario - COSTO_POR_LLAMADA, 4)
    user_data["credits_balance"] = nuevo_saldo
    db.set(user_key_path, user_data)
    
    # 4. Registrar ingreso en el Fondo Operativo / Liquidez de la Bóveda Soberana
    global_bal = db.get("global_sovereign_balance") or 0.0
    db.set("global_sovereign_balance", round(global_bal + COSTO_POR_LLAMADA, 4))
    
    # 5. Log de auditoría inmutable
    timestamp = datetime.now().isoformat()
    db.lpush("nexus_calls_log", f"[{timestamp}] API Key: {x_api_key[:6]}... | Costo: ${COSTO_POR_LLAMADA} | Saldo Restante: ${nuevo_saldo}")
    db.exportdb("backups/vault_backup.json")
    
    return {
        "status": "SUCCESS",
        "message": "Procesamiento completado por NEXUS-1",
        "prompt_received": prompt,
        "cost_deducted_usd": COSTO_POR_LLAMADA,
        "remaining_credits": nuevo_saldo
    }

@app.post("/nexus/v1/create-key")
async def registrar_nueva_api_key(client_name: str, initial_deposit: float):
    """Genera una nueva API Key corporativa y le asigna créditos iniciales."""
    import secrets
    api_key = f"nx_live_{secrets.token_hex(16)}"
    
    key_data = {
        "client_name": client_name,
        "credits_balance": initial_deposit,
        "created_at": datetime.now().isoformat()
    }
    
    db.set(f"api_keys_{api_key}", key_data)
    
    # Inyectar el depósito a la tesorería soberana
    global_bal = db.get("global_sovereign_balance") or 0.0
    db.set("global_sovereign_balance", round(global_bal + initial_deposit, 4))
    db.exportdb("backups/vault_backup.json")
    
    return {
        "status": "KEY_CREATED",
        "client": client_name,
        "api_key": api_key,
        "initial_credits_usd": initial_deposit
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
