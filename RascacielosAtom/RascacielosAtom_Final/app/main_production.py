import os
import elara
import json
from fastapi import FastAPI, Request, Header, HTTPException
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Rascacielos Digital Atom - Live Production Core",
    version="2.0.0",
    description="Motor central de monetización, tesorería fraccionada e industrial API Gateway (NEXUS-1)."
)

# Inicializar Bóveda Protegida en la ruta dedicada /vault
db = elara.exe_secure("vault/sovereign_vault.db", commitdb=True, key_path="vault/vault_master.key")

def aplicar_tesoreria_fraccionada(monto_real):
    """Distribuye automáticamente el dinero real bajo mejores prácticas de tesorería."""
    pct_crecimiento = 0.20  # Intocable para re-inversión
    pct_impuestos = 0.10    # Reserva SAT
    pct_operativa = 0.10    # Costos operativos
    pct_liquidez = 0.60     # Disponible para retiros a efectivo (Bitso/PayPal)

    monto_crecimiento = round(monto_real * pct_crecimiento, 2)
    monto_impuestos = round(monto_real * pct_impuestos, 2)
    monto_operativa = round(monto_real * pct_operativa, 2)
    monto_liquidez = round(monto_real * pct_liquidez, 2)

    bal_crecimiento = (db.get("vault_growth_untouchable") or 0.0) + monto_crecimiento
    bal_impuestos = (db.get("vault_tax_reserve") or 0.0) + monto_impuestos
    bal_operativa = (db.get("vault_ops_fund") or 0.0) + monto_operativa
    bal_liquidez = (db.get("global_sovereign_balance") or 0.0) + monto_liquidez

    db.set("vault_growth_untouchable", round(bal_crecimiento, 2))
    db.set("vault_tax_reserve", round(bal_impuestos, 2))
    db.set("vault_ops_fund", round(bal_operativa, 2))
    db.set("global_sovereign_balance", round(bal_liquidez, 2))

    timestamp = datetime.now().isoformat()
    db.lpush("live_transaction_logs", f"[{timestamp}] Ingreso REAL: +${monto_real} USD | Líquido: +${monto_liquidez} | Intocable: +${monto_crecimiento}")
    db.exportdb("backups/vault_backup.json")

    return {
        "status": "SUCCESS",
        "ingreso_usd": monto_real,
        "liquidez_disponible": bal_liquidez,
        "fondo_crecimiento_intocable": bal_crecimiento
    }

@app.post("/nexus/v1/execute")
async def nexus_execute(prompt: str, x_api_key: str = Header(...)):
    """API Gateway Industrial: Descuenta créditos por llamada en tiempo real."""
    user_key_path = f"api_keys_{x_api_key}"
    user_data = db.get(user_key_path)
    
    if not user_data:
        raise HTTPException(status_code=401, detail="API Key no autorizada en NEXUS-1.")
    
    costo_llamada = 0.05
    saldo_actual = user_data.get("credits_balance", 0.0)
    
    if saldo_actual < costo_llamada:
        raise HTTPException(status_code=403, detail="Créditos agotados. Recargue saldo en la Bóveda.")
    
    nuevo_saldo = round(saldo_actual - costo_llamada, 4)
    user_data["credits_balance"] = nuevo_saldo
    db.set(user_key_path, user_data)
    
    # Alimentar tesorería operativa
    global_bal = db.get("global_sovereign_balance") or 0.0
    db.set("global_sovereign_balance", round(global_bal + costo_llamada, 4))
    
    timestamp = datetime.now().isoformat()
    db.lpush("nexus_calls_log", f"[{timestamp}] Key: {x_api_key[:8]}... | Costo: ${costo_llamada} | Saldo: ${nuevo_saldo}")
    db.exportdb("backups/vault_backup.json")
    
    return {
        "status": "SUCCESS",
        "gateway": "NEXUS-1 Industrial",
        "prompt": prompt,
        "cost_usd": costo_llamada,
        "remaining_credits": nuevo_saldo
    }

@app.post("/nexus/v1/create-key")
async def nexus_create_key(client_name: str, initial_deposit: float):
    """Genera credenciales comerciales B2B y asegura el depósito en tesorería."""
    import secrets
    api_key = f"nx_live_{secrets.token_hex(16)}"
    
    key_data = {
        "client_name": client_name,
        "credits_balance": initial_deposit,
        "created_at": datetime.now().isoformat()
    }
    
    db.set(f"api_keys_{api_key}", key_data)
    aplicar_tesoreria_fraccionada(initial_deposit)
    
    return {
        "status": "API_KEY_ISSUED",
        "client": client_name,
        "api_key": api_key,
        "deposit_processed_usd": initial_deposit
    }

@app.post("/webhook/stripe-live")
async def stripe_webhook(request: Request):
    """Receptor oficial de transacciones monetarias reales vía Stripe."""
    try:
        payload = await request.json()
        if payload.get("type") == "payment_intent.succeeded":
            amount = payload["data"]["object"]["amount_received"] / 100.0
            resultado = aplicar_tesoreria_fraccionada(amount)
            return {"status": "processed", "details": resultado}
        return {"status": "event_ignored"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/vault/status")
async def vault_status():
    """Consulta en tiempo real el estado financiero de todas las sub-bóvedas."""
    return {
        "global_sovereign_balance_liquidez": db.get("global_sovereign_balance") or 0.0,
        "vault_growth_untouchable": db.get("vault_growth_untouchable") or 0.0,
        "vault_tax_reserve": db.get("vault_tax_reserve") or 0.0,
        "vault_ops_fund": db.get("vault_ops_fund") or 0.0
    }