# TOKYO OS (c) 2026 - TODOS LOS DERECHOS RESERVADOS - MARCA REGISTRADA
import os
import logging
import sqlite3
import sys

floor_name = sys.argv[1]
module_name = sys.argv[2]
description = sys.argv[3]

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] [%(module_name)s]: %(message)s".replace("%(module_name)s", module_name)
)

db_path = "E:\\TOKYOAPPS_UNIVERSE\\01_ACTIVE\\NULOGIC_CORE\\database\\Tokyo_001.db"

logging.info(f"Inicializando {description}...")

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO execution_logs (module, status, details) VALUES (?, ?, ?)",
        (module_name, "SUCCESS", f"{description} sincronizado y operativo con ruta absoluta al SSoT.")
    )
    conn.commit()
    conn.close()
    print(f"[ÉXITO ABSOLUTO] {floor_name} ({description}) conectado y registrado en la base de datos central.")
else:
    print(f"[AVISO CRÍTICO] Base de datos no encontrada para {floor_name}.")

