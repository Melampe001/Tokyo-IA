import sqlite3, datetime

DB_PATH = "Tokyo_001.db"

def upgrade_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. Tabla de Usuarios de Apps (Monetización)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS app_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            play_uid TEXT UNIQUE,
            email TEXT,
            tier TEXT DEFAULT 'FREE', 
            status TEXT DEFAULT 'ACTIVE',
            created_at TEXT,
            expires_at TEXT
        )
    """)
    conn.commit()
    conn.close()
    print("[✅] Esquema de monetización (APP_USERS) integrado en Tokyo_001.db")

def check_gating(play_uid, requested_feature):
    """
    Motor de Gatekeeping: Valida si el usuario tiene acceso a la función solicitada.
    Tiers: FREE (Básico), ONETIME (Full), PREMIUM (Suscripción Ilimitada)
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT tier, status, expires_at FROM app_users WHERE play_uid=?", (play_uid,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        return False, "User not found"

    tier, status, expires = user
    
    # Lógica de Validación (El "Gating")
    if status != 'ACTIVE':
        return False, "Account suspended"

    # Verificar expiración (si aplica)
    if expires and datetime.datetime.now() > datetime.datetime.strptime(expires, "%Y-%m-%d"):
        return False, "Subscription expired"

    # Matriz de Permisos
    permissions = {
        "FREE": ["export_low_res"],
        "ONETIME": ["export_low_res", "export_high_res", "commercial_rights"],
        "PREMIUM": ["export_low_res", "export_high_res", "commercial_rights", "ai_gen_unlimited"]
    }

    if requested_feature in permissions.get(tier, []):
        return True, "Access Granted"
    else:
        return False, f"Upgrade to {tier} required for {requested_feature}"

if __name__ == "__main__":
    upgrade_database()