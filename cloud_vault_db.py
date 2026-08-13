import sqlite3

DB_PATH = "Tokyo_001.db"

def init_cloud_vault():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Tabla para almacenar los logotipos creados por los usuarios de la app
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_logos (
            logo_id INTEGER PRIMARY KEY AUTOINCREMENT,
            play_uid TEXT,
            logo_name TEXT,
            logo_svg_data TEXT,
            palette_used TEXT,
            created_at TEXT,
            FOREIGN KEY (play_uid) REFERENCES app_users (play_uid)
        )
    """)
    conn.commit()
    conn.close()
    print("[✅] Tabla 'user_logos' (Cloud Vault) integrada correctamente en Tokyo_001.db")

if __name__ == "__main__":
    init_cloud_vault()