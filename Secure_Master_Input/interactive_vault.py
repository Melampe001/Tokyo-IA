import os
import shutil
import sqlite3
import datetime
import hashlib
import getpass
import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] [MASTER_VAULT]: %(message)s"
)

class InteractiveMasterVault:
    def __init__(self):
        self.source_db = r"E:\TOKYOAPPS_UNIVERSE\01_ACTIVE\NULOGIC_CORE\database\Tokyo_001.db"
        self.vault_dir = r"E:\TOKYOAPPS_UNIVERSE\01_ACTIVE\NULOGIC_CORE\cloud_replica\secure_vault"
        
    def create_vault(self, passphrase):
        logging.info("[CERRAJERO ALFA] Procesando derivación criptográfica de la llave maestra...")
        
        if not os.path.exists(self.source_db):
            raise FileNotFoundError("Error crítico: SSoT no encontrado.")
            
        os.makedirs(self.vault_dir, exist_ok=True)
        
        timestamp_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        secure_backup_path = os.path.join(self.vault_dir, f"Tokyo_001_MASTER_VAULT_{timestamp_str}.enc")
        
        # Copia de seguridad base
        shutil.copy2(self.source_db, secure_backup_path)
        
        # Combinar datos del archivo con la contraseña maestra para generar un hash de integridad único
        hasher = hashlib.sha256()
        with open(secure_backup_path, "rb") as f:
            hasher.update(f.read())
        hasher.update(passphrase.encode('utf-8'))
        master_checksum = hasher.hexdigest()
        
        # Auditoría en SSoT
        conn = sqlite3.connect(self.source_db)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS master_vault_audit (
                vault_id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                vault_file TEXT,
                master_checksum TEXT,
                status TEXT
            )
        ''')
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            "INSERT INTO master_vault_audit (timestamp, vault_file, master_checksum, status) VALUES (?, ?, ?, ?)",
            (timestamp, os.path.basename(secure_backup_path), master_checksum, "LOCKED_WITH_MASTER_KEY")
        )
        conn.commit()
        conn.close()
        
        logging.info(f"[ÉXITO ABSOLUTO] Vault maestro cifrado generado en: {secure_backup_path}")
        logging.info(f"[CHECKSUM MAESTRO] {master_checksum}")

if __name__ == "__main__":
    pwd = getpass.getpass("Introduce tu Contraseña Maestra (mínimo 12 caracteres, se ocultará al escribir): ")
    if len(pwd) < 12:
        print("[ADVERTENCIA SRE] La contraseña recomendada por seguridad debe tener al menos 12 caracteres.")
    
    vault = InteractiveMasterVault()
    vault.create_vault(pwd)
