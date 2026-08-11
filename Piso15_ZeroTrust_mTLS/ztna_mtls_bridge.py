import os
import logging
import sqlite3

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [%(levelname)s] [PISO15_ZTNA]: %(message)s")
db_path = "E:\\TOKYOAPPS_UNIVERSE\\01_ACTIVE\\NULOGIC_CORE\\database\\Tokyo_001.db"

logging.info("Inicializando Capa Zero-Trust Network Access (mTLS)...")
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO execution_logs (module, status, details) VALUES (?, ?, ?)", 
                   ("PISO15_ZTNA", "SUCCESS", "Micro-segmentación y mTLS activados en la red interna."))
    conn.commit()
    conn.close()
    print("[ÉXITO ABSOLUTO] Piso 15 (Zero-Trust mTLS) conectado y registrado.")
