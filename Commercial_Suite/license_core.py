import sqlite3
import datetime
import uuid
import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] [LICENSE_ENGINE]: %(message)s"
)

class LicenseEngine:
    def __init__(self):
        self.db_path = r"E:\TOKYOAPPS_UNIVERSE\01_ACTIVE\NULOGIC_CORE\database\Tokyo_001.db"

    def issue_license(self, email, full_name, tier="PRO", days=30):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Registrar cliente o recuperar ID
        cursor.execute("SELECT customer_id FROM flg_customers WHERE email = ?", (email,))
        row = cursor.fetchone()
        if row:
            customer_id = row[0]
        else:
            created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("INSERT INTO flg_customers (email, full_name, created_at) VALUES (?, ?, ?)", (email, full_name, created_at))
            customer_id = cursor.lastrowid
            
        # Generar Llave Única
        license_key = f"FLG-{str(uuid.uuid4()).upper()}"
        expires_at = (datetime.datetime.now() + datetime.timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S")
        
        cursor.execute(
            "INSERT INTO flg_licenses (customer_id, license_key, tier, status, expires_at) VALUES (?, ?, ?, ?, ?)",
            (customer_id, license_key, tier, "ACTIVE", expires_at)
        )
        conn.commit()
        conn.close()
        
        logging.info(f"[ÉXITO] Licencia emitida para {email} | Key: {license_key} | Expira: {expires_at}")
        return license_key

    def validate_license(self, license_key):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT status, expires_at FROM flg_licenses WHERE license_key = ?", (license_key,))
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            logging.warning("[ACCESO DENEGADO] La licencia no existe.")
            return False
            
        status, expires_at = row
        exp_date = datetime.datetime.strptime(expires_at, "%Y-%m-%d %H:%M:%S")
        
        if status == "ACTIVE" and datetime.datetime.now() <= exp_date:
            logging.info("[ACCESO CONCEDIDO] Licencia vigente y validada correctamente.")
            return True
        else:
            logging.warning("[ACCESO EXPIRADO] La licencia ha caducado o fue revocada.")
            return False

if __name__ == "__main__":
    engine = LicenseEngine()
    # Prueba automatizada de emisión y validación interna
    test_key = engine.issue_license("socio@flaggshipapps.com", "Jose Arturo Orozco Jaime", "FLAGGSHIP_MAX", 365)
    engine.validate_license(test_key)
