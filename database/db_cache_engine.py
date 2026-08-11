# TOKYO OS (c) 2026 - TODOS LOS DERECHOS RESERVADOS - MARCA REGISTRADA
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "nulogic_cache.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS system_cache (
            key TEXT PRIMARY KEY,
            value TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("[✅] Base de datos SQLite WAL inicializada correctamente.")

