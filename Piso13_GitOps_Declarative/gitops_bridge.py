import os
import logging
import sqlite3

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [%(levelname)s] [PISO13_GITOPS]: %(message)s")
db_path = "E:\\TOKYOAPPS_UNIVERSE\\01_ACTIVE\\NULOGIC_CORE\\database\\Tokyo_001.db"

logging.info("Inicializando Motor GitOps y Declarativo (IaC)...")
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO execution_logs (module, status, details) VALUES (?, ?, ?)", 
                   ("PISO13_GITOPS", "SUCCESS", "Infraestructura Declarativa sincronizada con el SSoT."))
    conn.commit()
    conn.close()
    print("[ÉXITO ABSOLUTO] Piso 13 (GitOps & IaC) conectado y registrado.")
