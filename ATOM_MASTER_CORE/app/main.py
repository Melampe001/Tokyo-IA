# TOKYO OS (c) 2026 - TODOS LOS DERECHOS RESERVADOS - MARCA REGISTRADA
import os
import hmac
import hashlib
import elara
from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from app.modules import floors
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="ATOM MASTER CORE - SECURE PRODUCTION")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(floors.router)

db = elara.exe_secure("vault/atom_sovereign.db", commitdb=True, key_path="vault/master.key")

STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "whsec_tu_secreto_real")

async def verificar_firma_stripe(request: Request):
    sig_header = request.headers.get("Stripe-Signature")
    body = await request.body()
    
    if not sig_header:
        raise HTTPException(status_code=400, detail="Falta la firma de seguridad de Stripe.")
    
    try:
        elements = dict(item.split("=", 1) for item in sig_header.split(","))
        timestamp = elements.get("t")
        v1_signature = elements.get("v1")
        
        if not timestamp or not v1_signature:
            raise HTTPException(status_code=400, detail="Cabecera Stripe-Signature malformada.")
            
        signed_payload = f"{timestamp}.".encode("utf-8") + body
        expected_sig = hmac.new(
            STRIPE_WEBHOOK_SECRET.encode("utf-8"),
            signed_payload,
            hashlib.sha256
        ).hexdigest()
        
        if not hmac.compare_digest(expected_sig, v1_signature):
            raise HTTPException(status_code=400, detail="Firma de webhook inválida o alterada.")
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en validación criptográfica: {str(e)}")

@app.post("/webhook/stripe-live")
async def stripe_webhook_secure(request: Request):
    await verificar_firma_stripe(request)
    payload = await request.json()
    if payload.get("type") == "payment_intent.succeeded":
        amount = payload["data"]["object"]["amount_received"] / 100.0
        saldo = db.get("global_balance") or 0.0
        nuevo_saldo = saldo + amount
        db.set("global_balance", nuevo_saldo)
        db.exportdb("vault/backup_vault.json")
        return {"status": "success", "amount_processed": amount, "new_vault_balance": nuevo_saldo}
    return {"status": "ignored_event"}

@app.get("/")
async def root(request: Request):
    balance = db.get("global_balance") or 0.0
    return templates.TemplateResponse("master_panel.html", {
        "request": request,
        "balance": f"{balance:,.2f}",
        "status": "SECURE PRODUCTION - TUNNEL READY"
    })
