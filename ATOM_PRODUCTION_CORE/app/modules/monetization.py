from fastapi import APIRouter
import elara

router = APIRouter(prefix="/nexus/monetization", tags=["Monetización"])
db = elara.exe_secure("vault/atom_sovereign.db", commitdb=True, key_path="vault/master.key")

@router.post("/ingestar-impresiones")
async def ingestar(impresiones: int, rpm: float = 4.50):
    ingreso = round((impresiones / 1000.0) * rpm, 4)
    balance = db.get("global_balance") or 0.0
    nuevo = round(balance + ingreso, 2)
    db.set("global_balance", nuevo)
    db.exportdb("vault/backup_vault.json")
    return {"status": "TRAFFIC MONETIZED", "ingreso": ingreso, "saldo": nuevo}