import sqlite3
import json
import datetime
from pathlib import Path

BASE_DIR = Path(r"E:\TOKYOAPPS_UNIVERSE\01_ACTIVE\NULOGIC_CORE")
DB_TELEMETRY = BASE_DIR / "telemetry" / "telemetry_audit.sqlite"
MEMORIA_FILE = BASE_DIR / "memoria" / "estado_persistente.json"

print("=" * 70)
print("     NULOGIC CORE :: AUDITORIA DE INTEGRIDAD DE ACTIVOS 24/7     ")
print("=" * 70)

# 1. VERIFICACIÓN DE PISO 01: PERSISTENCIA E IDEMPOTENCIA (JSON)
print("\n[PISO 01] -> ESTADO PERSISTENTE EN MEMORIA (JSON)")
if MEMORIA_FILE.exists():
    try:
        with open(MEMORIA_FILE, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
            keys = data.get("processed_keys", {})
            print(f"  • Claves Idempotentes Registradas: {len(keys)}")
            print("  • Últimas Operaciones Evitadas/Garantizadas:")
            for k, v in list(keys.items())[-3:]:
                ord_id = v.get("ordId", "N/A")
                status = v.get("state", "N/A")
                print(f"    - Hash: {k[:16]}... | Orden: {ord_id} | Estado: {status}")
    except Exception as e:
        print(f"  ! Error leyendo memoria JSON: {e}")
else:
    print("  ! Archivo estado_persistente.json aún no creado (se creará al iniciar el motor).")

# 2. VERIFICACIÓN DE PISO 09: TELEMETRÍA Y AUDITORÍA FINANCIERA (SQLITE)
print("\n[PISO 09] -> TELEMETRIA DE TRANSACCIONES (SQLITE)")
if DB_TELEMETRY.exists():
    try:
        conn = sqlite3.connect(DB_TELEMETRY)
        cursor = conn.cursor()
        cursor.execute("SELECT id, timestamp, floor, event_type, payload FROM audit_logs ORDER BY id DESC LIMIT 5")
        rows = cursor.fetchall()
        if rows:
            print(f"  {'ID':<5} | {'HORA REGISTRO':<19} | {'PISO':<8} | {'EVENTO':<15} | {'ORDEN ID'}")
            print("  " + "-" * 66)
            for row in rows:
                dt = datetime.datetime.fromtimestamp(row[1]).strftime('%Y-%m-%d %H:%M:%S')
                payload = json.loads(row[4])
                ord_id = payload.get('ordId', 'N/A')
                print(f"  {row[0]:<5} | {dt:<19} | {row[2]:<8} | {row[3]:<15} | {ord_id}")
        else:
            print("  ! La tabla audit_logs no contiene registros aún.")
        conn.close()
    except Exception as e:
        print(f"  ! Error consultando la base de datos SQLite: {e}")
else:
    print("  ! Archivo telemetry_audit.sqlite no encontrado (se creará al iniciar el motor).")

print("\n" + "=" * 70)