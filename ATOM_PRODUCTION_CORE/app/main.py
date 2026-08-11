# TOKYO OS (c) 2026 - TODOS LOS DERECHOS RESERVADOS - MARCA REGISTRADA
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from app.modules import floors, dropshipping, monetization
import elara

app = FastAPI(title="ATOM PRODUCTION CORE - MASTER UNIFIED", version="5.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(floors.router)
app.include_router(dropshipping.router)
app.include_router(monetization.router)

db = elara.exe_secure("vault/atom_sovereign.db", commitdb=True, key_path="vault/master.key")

@app.get("/")
async def root(request: Request):
    balance = db.get("global_balance") or 0.0
    return templates.TemplateResponse(request, "dashboard.html", {"balance": f"{balance:,.2f}"})
