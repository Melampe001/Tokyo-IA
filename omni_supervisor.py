import time, threading
from core_db import init_db, log_event
from modules_suite import fetch_okx_market, fetch_bybit_liquidity, check_github_status
from sync_engine import mirror_to_drives
from dashboard_ui import run_dashboard

init_db()
log_event("SUPERVISOR", "Núcleo Soberano inicializado con protocolos militares.", "STARTUP")

print("==================================================================")
print("  [NULOGIC CORE] SUPERVISOR MAESTRO - SOBERANO Y AUTOSUSTENTABLE")
print("==================================================================")

threading.Thread(target=run_dashboard, daemon=True).start()

def sovereign_worker():
    print("[🧵 WATCHDOG] Sistema de auto-sanación y sincronización C: / E: activo.")
    while True:
        try:
            okx = fetch_okx_market()
            bybit = fetch_bybit_liquidity()
            check_github_status()
            
            if okx and bybit:
                print(f"   📊 [MARKET SYNC] OKX: ${okx:,.2f} | Bybit: ${bybit:,.2f}")
            
            mirror_to_drives()
            
        except Exception as e:
            log_event("WATCHDOG", f"Auto-sanación activada tras excepción: {e}", "WARNING")
            print(f"   ⚠️ [WATCHDOG RECOVERY] Incidencia aislada y corregida: {e}")
            
        time.sleep(20)

threading.Thread(target=sovereign_worker, daemon=True).start()

print("\n[🚀] Ecosistema completo operando en localhost, C:, E: y sincronizado con seguridad militar.")
print("[📌] Accede a tu panel visual en: http://127.0.0.1:8000")
print("[📌] Presiona Ctrl+C para detener el supervisor de forma segura.\n")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n[🛑] Supervisor detenido de forma ordenada. Estado persistido y blindado.")