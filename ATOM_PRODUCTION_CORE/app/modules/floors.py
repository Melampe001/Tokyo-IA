from fastapi import APIRouter, BackgroundTasks, HTTPException
import elara
from datetime import datetime

router = APIRouter(prefix="/nexus", tags=["Centro Financiero"])
db = elara.exe_secure("vault/atom_sovereign.db", commitdb=True, key_path="vault/master.key")

@router.post("/liquidar-ingreso")
async def liquidar_ingreso(monto: float = 1557.34):
    saldo = db.get("global_balance") or 0.0
    nuevo = round(saldo + monto, 2)
    db.set("global_balance", nuevo)
    db.exportdb("vault/backup_vault.json")
    return {"status": "LIQUIDADO", "monto": monto, "saldo": nuevo}

@router.post("/disponer-efectivo")
async def disponer_efectivo(monto: float):
    saldo = db.get("global_balance") or 0.0
    if monto > saldo:
        raise HTTPException(status_code=400, detail="Fondos insuficientes en Bóveda.")
    nuevo = round(saldo - monto, 2)
    db.set("global_balance", nuevo)
    db.exportdb("vault/backup_vault.json")
    return {"status": "RETIRADO", "monto": monto, "saldo": nuevo}