import os
import sqlite3
import logging

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [%(levelname)s] [TRADEMARK_SYNC]: %(message)s")

db_path = "E:\\TOKYOAPPS_UNIVERSE\\01_ACTIVE\\NULOGIC_CORE\\database\\Tokyo_001.db"
official_name = "Rascacielos Digital Atom®"
owner = "Jose Arturo Orozco Jaime (Tokyo)"
github_user = "Melampe001"

logging.info(f"Actualizando identidad corporativa a: {official_name}")

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Registrar la actualización de marca en el SSoT
    cursor.execute(
        "INSERT INTO execution_logs (module, status, details) VALUES (?, ?, ?)",
        ("TRADEMARK_UPDATE", "SUCCESS", f"Identidad oficial actualizada: {official_name} | Propietario: {owner} | GitHub: {github_user}")
    )
    conn.commit()
    conn.close()
    print("[ÉXITO ABSOLUTO] Rascacielos Digital Atom® registrado y sincronizado en el SSoT.")
else:
    print("[ERROR CRÍTICO] SSoT no localizado en la ruta base.")
