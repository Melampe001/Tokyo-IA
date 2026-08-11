from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from app.modules import floors
import elara

app = FastAPI(title="NEXUS-1 MASTER CORE")

# Configuración de CORS para permitir acceso global seguro [1, 6]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Incluimos el router modular para evitar errores 404 [3, 4]
app.include_router(floors.router)

db = elara.exe_secure("vault/atom_sovereign.db", commitdb=True, key_path="vault/master.key")

@app.get("/")
async def root(request: Request):
    balance = db.get("global_balance") or 0.0
    return templates.TemplateResponse("panel.html", {
        "request": request,
        "balance": f"{balance:,.2f}",
        "status": "BUILDING SEALED - PRODUCTION READY"
    })
