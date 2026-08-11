# TOKYO OS (c) 2026 - TODOS LOS DERECHOS RESERVADOS - MARCA REGISTRADA
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from app.modules import nexus
import elara

app = FastAPI(title="ATOM MASTER CORE")

# Configuración de CORS alineada a estándares mundiales de interoperabilidad
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
app.include_router(nexus.router)

db = elara.exe_secure("vault/atom_sovereign.db", commitdb=True, key_path="vault/master.key")

@app.get("/")
async def dashboard(request: Request):
    saldos = db.get("floor_balances") or {str(i): 0.0 for i in range(1, 13)}
    logs = db.get("audit_trail") or []
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "saldos": saldos,
        "total": sum(saldos.values()),
        "logs": logs[:5]
    })

