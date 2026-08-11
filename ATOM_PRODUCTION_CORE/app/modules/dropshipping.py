# TOKYO OS (c) 2026 - TODOS LOS DERECHOS RESERVADOS - MARCA REGISTRADA
from fastapi import APIRouter, HTTPException
import elara, uuid

router = APIRouter(prefix="/nexus/dropshipping", tags=["Dropshipping"])
db = elara.exe_secure("vault/atom_sovereign.db", commitdb=True, key_path="vault/master.key")

@router.post("/procesar-orden")
async def procesar_orden(sku: str, costo: float, venta: float):
    balance = db.get("global_balance") or 0.0
    if costo > balance:
        raise HTTPException(status_code=400, detail="Saldo insuficiente para costo mayorista.")
    ganancia = round(venta - costo, 2)
    nuevo = round(balance + ganancia, 2)
    db.set("global_balance", nuevo)
    db.exportdb("vault/backup_vault.json")
    return {"status": "ORDEN DISPATCHED", "order_id": f"DS-{str(uuid.uuid4())[:6].upper()}", "ganancia": ganancia, "saldo": nuevo}
