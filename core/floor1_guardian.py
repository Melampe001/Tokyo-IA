# TOKYO OS (c) 2026 - TODOS LOS DERECHOS RESERVADOS - MARCA REGISTRADA
import os
import shutil
import datetime
import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] [FLOOR1_GUARDIAN]: %(message)s"
)

def create_atomic_backup():
    # Usamos ruta absoluta basada en la estructura del monorepo
    base_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(base_dir)
    
    db_source = os.path.join(root_dir, "database", "Tokyo_001.db")
    backup_dir = os.path.join(root_dir, "vault", "backups")
    os.makedirs(backup_dir, exist_ok=True)
    
    if os.path.exists(db_source):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(backup_dir, f"Tokyo_001_backup_{timestamp}.db")
        shutil.copy2(db_source, backup_path)
        logging.info(f"Respaldo atómico de seguridad generado con éxito en: {backup_path}")
    else:
        logging.warning(f"[AVISO] No se encontró la base de datos principal en la ruta: {db_source}")

if __name__ == "__main__":
    create_atomic_backup()

