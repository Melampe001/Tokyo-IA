import sqlite3
import datetime
import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] [COMMERCIAL_CORE]: %(message)s"
)

class CommercialLicenseManager:
    def __init__(self):
        self.db_path = r"E:\TOKYOAPPS_UNIVERSE\01_ACTIVE\NULOGIC_CORE\database\Tokyo_001.db"
        self.initialize_license_tables()

    def initialize_license_tables(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabla de Clientes / Suscriptores
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS flg_customers (
                customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE,
                full_name TEXT,
                created_at TEXT
            )
        ''')
        
        # Tabla de Licencias Activas (SaaS)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS flg_licenses (
                license_id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER,
                license_key TEXT UNIQUE,
                tier TEXT,
                status TEXT,
                expires_at TEXT,
                FOREIGN KEY(customer_id) REFERENCES flg_customers(customer_id)
            )
        ''')
        
        conn.commit()
        conn.close()
        logging.info("[ÉXITO ABSOLUTO] Tablas comerciales y de licenciamiento desplegadas en el SSoT.")

if __name__ == "__main__":
    manager = CommercialLicenseManager()
