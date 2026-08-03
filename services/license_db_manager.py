import sqlite3
import os
import uuid
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "database", "licenses.db")

PRODUCTS_CATALOG = {
    "A": {"id": "TRADING_BOT_PRO", "name": "RascaCielos-Digital® Trading Bot VIP", "price": 99.99, "duration": 30},
    "B": {"id": "SAAS_BOILERPLATE", "name": "RascaCielos-Digital® Backend SaaS Template", "price": 149.99, "duration": 3650},
    "C": {"id": "VIP_MEMBERSHIP", "name": "RascaCielos-Digital® VIP Signal & Newsletter", "price": 29.99, "duration": 30},
    "D": {"id": "DEVOPS_SUITE", "name": "RascaCielos-Digital® DevOps & PowerShell Suite", "price": 79.99, "duration": 365}
}

class LicenseManager:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS licenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    license_key TEXT UNIQUE NOT NULL,
                    customer_name TEXT NOT NULL,
                    customer_email TEXT NOT NULL,
                    product_code TEXT NOT NULL,
                    product_name TEXT NOT NULL,
                    amount_paid REAL NOT NULL,
                    currency TEXT DEFAULT 'USD',
                    status TEXT CHECK(status IN ('ACTIVE', 'SUSPENDED', 'EXPIRED', 'REVOKED')) DEFAULT 'ACTIVE',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP
                )
            ''')
            conn.commit()

    def generate_product_license(self, product_key, customer_name, customer_email, custom_price=None):
        prod = PRODUCTS_CATALOG.get(product_key, PRODUCTS_CATALOG["B"])
        raw_uuid = str(uuid.uuid4()).upper().replace("-", "")
        license_key = f"RASCACIELOS-{prod['id'][:4]}-{raw_uuid[:4]}-{raw_uuid[4:8]}"
        
        amount = custom_price if custom_price else prod["price"]
        expires_at = datetime.now() + timedelta(days=prod["duration"])

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO licenses (license_key, customer_name, customer_email, product_code, product_name, amount_paid, expires_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (license_key, customer_name, customer_email, prod["id"], prod["name"], amount, expires_at.strftime("%Y-%m-%d %H:%M:%S")))
            conn.commit()

        return license_key, prod

    def verify_license(self, license_key):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM licenses WHERE license_key = ?", (license_key,))
            license = cursor.fetchone()
            if not license:
                return False, "Licencia no encontrada."
            if license['status'] != 'ACTIVE':
                return False, f"Estado de licencia: {license['status']}."
            return True, dict(license)
