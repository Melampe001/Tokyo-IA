# TOKYO OS (c) 2026 - TODOS LOS DERECHOS RESERVADOS - MARCA REGISTRADA
import os
import sqlite3
import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] [TOKYO_PERSISTENCE]: %(message)s"
)

class TokyoDatabaseCore:
    def __init__(self):
        self.db_path = "../database/Tokyo_001.db"
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS execution_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                module TEXT,
                status TEXT,
                details TEXT
            )
        """)
        conn.commit()
        conn.close()
        logging.info(f"Base de datos central verificada en: {self.db_path}")

    def log_event(self, module, status, details):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO execution_logs (module, status, details) VALUES (?, ?, ?)",
            (module, status, details)
        )
        conn.commit()
        conn.close()
        logging.info("Evento registrado de forma atómica en Tokyo_001.db")

if __name__ == "__main__":
    db = TokyoDatabaseCore()
    db.log_event("MONETIZATION_CORE", "SUCCESS", "Pipeline y Ejecutor sincronizados al 100%")

