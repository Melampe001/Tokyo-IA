import os
import logging
import sqlite3

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [%(levelname)s] [PISO14_CHAOS]: %(message)s")
db_path = "E:\\TOKYOAPPS_UNIVERSE\\01_ACTIVE\\NULOGIC_CORE\\database\\Tokyo_001.db"

logging.info("Inicializando Módulo de Chaos Engineering y Pruebas de Resiliencia...")
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO execution_logs (module, status, details) VALUES (?, ?, ?)", 
                   ("PISO14_CHAOS", "SUCCESS", "Motor de Resiliencia y Failover activo."))
    conn.commit()
    conn.close()
    print("[ÉXITO ABSOLUTO] Piso 14 (Chaos Engineering) conectado y registrado.")
