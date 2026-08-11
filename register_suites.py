# TOKYO OS (c) 2026 - TODOS LOS DERECHOS RESERVADOS - MARCA REGISTRADA
import sqlite3, datetime

DB_PATH = "Tokyo_001.db"

def register_all_suites():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        suites = [
            "Piso1_Kernel_Cognitivo", "Piso2_Trading_Autonomo", "Piso3_Finanzas_Corp",
            "Piso4_Gobierno_Leyes", "Piso5_Live_Sync_Hub", "Piso6_Motor_Industrial",
            "Piso7_Seguridad_Militar", "Piso8_Ecosistema_Medico", "Piso9_SYNEMU_Suite",
            "Piso10_FlaggShip_Apps", "Piso11_Nexus_Orchestrator", "Piso12_Global_Core",
            "ATOM_MASTER_CORE", "ATOM_PRODUCTION_CORE", "ATOM_SOVEREIGN_CORE", "ATOM_TOTAL_SYSTEM"
        ]
        
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for s in suites:
            cursor.execute("""
                INSERT INTO sovereign_states (suite_name, status, last_active, metrics) 
                VALUES (?, ?, ?, ?)
                ON CONFLICT(suite_name) DO UPDATE SET status=excluded.status, last_active=excluded.last_active
            """, (s, "ACTIVE", now, "Fully Synchronized"))
            
        conn.commit()
        conn.close()
        print("   [DB] Todos los estados de las suites han sido persistidos en Tokyo_001.db.")
    except Exception as e:
        print(f"   [DB ERROR] {e}")

if __name__ == "__main__":
    register_all_suites()
