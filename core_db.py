# TOKYO OS (c) 2026 - TODOS LOS DERECHOS RESERVADOS - MARCA REGISTRADA
import sqlite3, datetime, os, hashlib

DB_PATH = "Tokyo_001.db"

def init_db():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Tabla principal de telemetría y logs
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS system_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                module TEXT,
                message TEXT,
                status TEXT,
                checksum TEXT
            )
        """)
        
        # Tabla para persistencia de estados de suites y agentes autónomos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sovereign_states (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                suite_name TEXT UNIQUE,
                status TEXT,
                last_active TEXT,
                metrics TEXT
            )
        """)
        
        # Migración dinámica de esquema para evitar inconsistencias históricas
        cursor.execute("PRAGMA table_info(system_logs)")
        columns = [info[1] for info in cursor.fetchall()]
        if "checksum" not in columns:
            cursor.execute("ALTER TABLE system_logs ADD COLUMN checksum TEXT")

        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[DB INIT ERROR] {e}")

def log_event(module, message, status="INFO"):
    try:
        init_db()
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        raw_data = f"{now}{module}{message}{status}"
        checksum = hashlib.sha256(raw_data.encode()).hexdigest()
        
        cursor.execute("INSERT INTO system_logs (timestamp, module, message, status, checksum) VALUES (?, ?, ?, ?, ?)",
                       (now, module, message, status, checksum))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[DB WRITE ERROR] {e}")

def update_suite_state(suite_name, status, metrics="OK"):
    try:
        init_db()
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            INSERT INTO sovereign_states (suite_name, status, last_active, metrics) 
            VALUES (?, ?, ?, ?)
            ON CONFLICT(suite_name) DO UPDATE SET status=excluded.status, last_active=excluded.last_active, metrics=excluded.metrics
        """, (suite_name, status, now, metrics))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[STATE ERROR] {e}")
