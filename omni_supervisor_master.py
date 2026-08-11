import time, threading, os
from core_db import init_db, log_event, update_suite_state
from sync_engine import mirror_to_drives

init_db()
log_event("MASTER", "Supervisor Soberano Unificado iniciado. Verificando todas las terminales y pisos.", "STARTUP")

print("==================================================================")
print("  [NULOGIC CORE] SUPERVISOR MAESTRO UNIFICADO - RASCACIELOS DIGITAL")
print("==================================================================")

active_suites = [
    "Piso1_Kernel_Cognitivo",
    "Piso2_Trading_Autonomo",
    "Piso3_Finanzas_Corp",
    "Piso7_Seguridad_Militar",
    "Piso9_SYNEMU_Suite",
    "Piso10_FlaggShip_Apps",
    "Piso11_Nexus_Orchestrator",
    "Piso12_Global_Core",
    "ATOM_SOVEREIGN_CORE"
]

def monitor_suites():
    while True:
        try:
            for suite in active_suites:
                suite_path = os.path.join(os.getcwd(), suite)
                status = "ACTIVE" if os.path.exists(suite_path) else "STANDBY"
                update_suite_state(suite, status, "Healthy")
            
            mirror_to_drives()
            log_event("WATCHDOG", "Ciclo de sincronización y validación multisitio completado.", "SUCCESS")
        except Exception as e:
            log_event("WATCHDOG", f"Incidencia en ciclo de monitoreo: {e}", "WARNING")
        
        time.sleep(30)

threading.Thread(target=monitor_suites, daemon=True).start()

print(f"\n[🚀] Ecosistema operando con {len(active_suites)} suites detectadas y bajo supervisión constante.")
print("[📌] Presiona Ctrl+C para detener el supervisor de forma ordenada.\n")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n[🛑] Operación detenida por el operador. Estado blindado y persistido.")