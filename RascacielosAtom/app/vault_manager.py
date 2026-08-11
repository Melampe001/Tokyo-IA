import elara
import json
from datetime import datetime

# Inicializar Bóveda Protegida (Piso 7)
# commitdb=True asegura que el dinero se guarde físicamente al instante
db = elara.exe_secure("sovereign_vault.db", commitdb=True, key_path="vault_master.key")

def registrar_liquidacion(total_ciclo):
    # Recuperar saldo actual o iniciar en 0.0 si es la primera vez
    saldo_actual = db.get("global_sovereign_balance")
    if saldo_actual is None:
        saldo_actual = 0.0
    
    # Lógica de acumulación
    nuevo_total = saldo_actual + total_ciclo
    db.set("global_sovereign_balance", nuevo_total)
    
    # Registrar log de auditoría inmutable
    timestamp = datetime.now().isoformat()
    db.lpush("history_logs", f"[{timestamp}] Liquidación: + | Nuevo Total: ")
    
    # Crear respaldo externo (DRP) para seguridad adicional
    db.exportdb("backups/vault_backup.json")
    
    return nuevo_total

# Ejecución de la liquidación actual detectada por el OMNI-DAEMON
total_detectado = 1557.34
total_acumulado = registrar_liquidacion(total_detectado)

print(f"--- BÓVEDA ACTUALIZADA ---")
print(f"Saldo Anterior: ")
print(f"Inyección Actual: ")
print(f"SALDO SOBERANO TOTAL: ")
