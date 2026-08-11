# TOKYO OS (c) 2026 - TODOS LOS DERECHOS RESERVADOS - MARCA REGISTRADA
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from app.modules import floors
import elara

app = FastAPI(title="ATOM MASTER CORE")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
app.include_router(floors.router)

db = elara.exe_secure("vault/atom_sovereign.db", commitdb=True, key_path="vault/master.key")

@app.get("/")
async def root(request: Request):
    balance = db.get("global_balance") or 0.0
    return templates.TemplateResponse("panel.html", {"request": request, "balance": f"{balance:,.2f}"})
