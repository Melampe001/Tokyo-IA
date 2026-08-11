# TOKYO OS (c) 2026 - TODOS LOS DERECHOS RESERVADOS - MARCA REGISTRADA
import sqlite3, time, os

DB_PATH = "Tokyo_001.db"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def render_hud():
    while True:
        clear_screen()
        print("==================================================================")
        print("  [BI-SI HUD] RASCACIELOS DIGITAL - TELEMETRÍA 360° ALFA-OMEGA     ")
        print("==================================================================")
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute("SELECT suite_name, status, last_active FROM sovereign_states")
            states = cursor.fetchall()
            
            print(f"\n[🏢] ESTADO DE SUITES Y PISOS ACTIVOS ({len(states)} registrados):")
            print("-" * 65)
            print(f"{'SUITE / PISO':<30} | {'ESTADO':<10} | {'ÚLTIMA ACTIVIDAD'}")
            print("-" * 65)
            for suite, status, active in states:
                status_icon = "🟢" if status == "ACTIVE" else "🟡"
                print(f"{suite:<30} | {status_icon} {status:<7} | {active}")
                
            print("\n[🛡️] ÚLTIMOS EVENTOS REGISTRADOS:")
            print("-" * 65)
            cursor.execute("SELECT timestamp, module, message, status FROM system_logs ORDER BY id DESC LIMIT 5")
            logs = cursor.fetchall()
            for ts, mod, msg, stat in logs:
                print(f"[{ts}] [{mod}] ({stat}): {msg}")
                
            conn.close()
        except Exception as e:
            print(f"[HUD ERROR] Leyendo base de datos: {e}")
            
        print("\n[📌] Actualizando cada 5 segundos. Presiona Ctrl+C para salir.")
        time.sleep(5)

if __name__ == "__main__":
    try:
        render_hud()
    except KeyboardInterrupt:
        print("\n[👋] HUD finalizado de forma ordenada.")
