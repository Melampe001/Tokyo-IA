# TOKYO OS (c) 2026 - TODOS LOS DERECHOS RESERVADOS - MARCA REGISTRADA
import shutil, os
from core_db import log_event

def mirror_to_drives():
    src_db = "Tokyo_001.db"
    mirror_dir = r"C:\NULOGIC_MIRROR"
    dst_db = os.path.join(mirror_dir, "Tokyo_001.db")
    try:
        if not os.path.exists(mirror_dir):
            os.makedirs(mirror_dir, exist_ok=True)
        if os.path.exists(src_db):
            shutil.copy2(src_db, dst_db)
            log_event("SYNC", "Espejo multisitio C: actualizado correctamente", "SUCCESS")
    except Exception as e:
        log_event("SYNC", f"Error de replicación en C:: {e}", "ERROR")
