from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import elara
import os
from datetime import datetime

app = FastAPI(title="NEXUS-1: Orquestador Global Atom")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Bóveda de Seguridad (Piso 7) - Persistencia Atómica y Cifrado
db = elara.exe_secure("vault/atom_sovereign.db", commitdb=True, key_path="vault/master.key")

# Inicializar balances si no existen
if db.get("global_balance") is None:
    db.set("global_balance", 0.0)

# Lógica de Monetización (Pisos 10 y 11)
@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    current_balance = db.get("global_balance")
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "balance": f"{current_balance:,.2f}",
        "status": "ONLINE 24/7"
    })

@app.post("/liquidar/{monto}")
async def liquidar_ciclo(monto: float):
    # Acumulación de riqueza soberana
    saldo_anterior = db.get("global_balance")
    nuevo_saldo = saldo_anterior + monto
    db.set("global_balance", nuevo_saldo)
    
    # Log de auditoría inmutable
    log_entry = f"[{datetime.now().isoformat()}] + | Total: "
    if not db.exists("audit_logs"):
        db.lnew("audit_logs")
    db.lpush("audit_logs", log_entry)
    
    return {"status": "Liquidación Exitosa", "nuevo_total": nuevo_saldo}

@app.get("/descarga-premium/{id}")
async def delivery(id: str):
    # Entrega de activos mediante FileResponse optimizado
    return FileResponse(path=f"static/assets/premium_{id}.png", filename=f"atom_asset_{id}.png")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, workers=4)
