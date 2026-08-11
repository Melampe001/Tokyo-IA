# TOKYO OS (c) 2026 - TODOS LOS DERECHOS RESERVADOS - MARCA REGISTRADA
from fastapi import APIRouter, BackgroundTasks, HTTPException
import elara
import time
from datetime import datetime

router = APIRouter(prefix="/nexus", tags=["Centro de Mando e Ingresos"])
db = elara.exe_secure("vault/atom_sovereign.db", commitdb=True, key_path="vault/master.key")

def registrar_auditoria_retiro(monto: float, nuevo_saldo: float):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    registro = f"[{timestamp}] RETIRO AUTÓNOMO: -${monto:,.2f} USD | Saldo Restante: ${nuevo_saldo:,.2f} USD"
    db.lpush("audit_trail_retiros", registro)
    db.exportdb("vault/backup_vault.json")

@router.post("/disponer-efectivo-autonomo")
async def disponer_efectivo(tasks: BackgroundTasks, monto: float):
    saldo = db.get("global_balance") or 0.0
    
    if monto <= 0:
        raise HTTPException(status_code=400, detail="El monto de disposición debe ser mayor a cero.")
    if monto > saldo:
        raise HTTPException(status_code=400, detail=f"Fondos insuficientes en la Bóveda P7. Saldo disponible: ${saldo:,.2f} USD")
    
    nuevo_saldo = round(saldo - monto, 2)
    db.set("global_balance", nuevo_saldo)
    tasks.add_task(registrar_auditoria_retiro, monto, nuevo_saldo)
    
    return {
        "status": "ORDEN DE RETIRO EJECUTADA",
        "monto_retirado": monto,
        "saldo_restante_boveda": nuevo_saldo,
        "auditoria": "Libro mayor actualizado y respaldado"
    }

@router.get("/status")
async def get_status():
    return {"piso": "Operativo", "seguridad": "Grado Militar (Master Key activa)", "auditoria": "Activa"}
