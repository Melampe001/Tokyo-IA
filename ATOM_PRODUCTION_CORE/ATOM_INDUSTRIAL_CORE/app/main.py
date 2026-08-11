# TOKYO OS (c) 2026 - TODOS LOS DERECHOS RESERVADOS - MARCA REGISTRADA
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.modules import nexus, optimization
import elara

app = FastAPI(title="ATOM INDUSTRIAL PRODUCTION", version="6.0")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(nexus.router)

db = elara.exe_secure("vault/atom_sovereign.db", commitdb=True, key_path="vault/master.key")

@app.get("/")
async def dashboard(request: Request):
    saldos = db.get("floor_balances") or {str(i): 0.0 for i in range(1, 13)}
    saldos_str = {str(k): float(v) for k, v in saldos.items()}
    total = sum(saldos_str.values())
    logs = db.get("audit_trail") or []
    return templates.TemplateResponse("dashboard.html", {
        "request": request, "total": total, "saldos": saldos_str, "logs": logs
    })
