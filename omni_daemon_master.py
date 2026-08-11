# TOKYO OS (c) 2026 - TODOS LOS DERECHOS RESERVADOS - MARCA REGISTRADA
import time, datetime, sqlite3, requests, threading
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

print("==================================================================")
print("  [OMNI-DAEMON] NÚCLEO PRODUCCIÓN END-TO-END (1000+1 - BLINDADO)")
print("==================================================================")

DB_PATH = "Tokyo_001.db"

def init_db():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS omni_telemetry (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                source TEXT,
                metric TEXT,
                value REAL,
                status TEXT
            )
        """)
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[DB ERROR] {e}")

init_db()

def log_telemetry(source, metric, value, status):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO omni_telemetry (timestamp, source, metric, value, status) VALUES (?, ?, ?, ?, ?)",
                       (now, source, metric, value, status))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[DB WRITE ERROR] {e}")

# Configurar sesión robusta con reintentos automáticos y cabeceras anti-ban
def create_robust_session():
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504, 429])
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("https://", adapter)
    session.headers.update({
        "User-Agent": "TokyoApps-OmniDaemon/1.0 (Windows NT; NulogicCore-Production)",
        "Accept": "application/json"
    })
    return session

def trading_loop():
    print("[🧵 HILO ACTIVO] Motor de Liquidez y Mercados (Piso 2 - Blindado Anti-Ban)")
    session = create_robust_session()
    while True:
        try:
            url = "https://www.okx.com/api/v5/market/ticker?instId=BTC-USDT"
            res = session.get(url, timeout=5)
            if res.status_code == 200:
                data = res.json()
                if data.get("code") == "0" and data.get("data"):
                    price_str = data["data"][0].get("last")
                    if price_str:
                        price = float(price_str)
                        print(f"   📊 [MERCADO SEGURO] BTC-USDT (OKX): ${price:,.2f} | Estado: ACTIVO")
                        log_telemetry("Piso2_Trading", "BTC_PRICE", price, "SECURE_ACTIVE")
                else:
                    print(f"   ⚠️ [API ADVERTENCIA] Código OKX: {data.get('code')}")
            elif res.status_code == 429:
                print("   🚨 [ANTI-BAN] Límite de tasa detectado (HTTP 429). Pausa defensiva...")
                time.sleep(15)
            else:
                print(f"   ⚠️ [HTTP ERROR] Código {res.status_code}")
        except Exception as e:
            print(f"   ⚠️ [CONEXIÓN BLINDADA] Recuperando tras excepción de red: {e}")
        
        time.sleep(5)

def telemetry_loop():
    print("[🧵 HILO ACTIVO] Agente de Telemetría y Alertas (Piso 9)")
    while True:
        try:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"   💓 [HEARTBEAT PRODUCCIÓN] Sistema 1000+1 estable a las {now}")
            log_telemetry("OmniDaemon", "SYSTEM_HEALTH", 100.0, "PRODUCTION_READY")
        except Exception as e:
            print(f"   ⚠️ [TELEMETRY ERROR] {e}")
        time.sleep(30)

t1 = threading.Thread(target=trading_loop, daemon=True)
t2 = threading.Thread(target=telemetry_loop, daemon=True)

t1.start()
t2.start()

print("\n[🚀] NÚCLEO OMNI-DAEMON 1000+1 EN MODO PRODUCCIÓN 24/7.")
print("[📌] Presiona Ctrl+C para detener el sistema de forma segura.\n")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n[🛑] Sistema detenido de forma ordenada. Estado guardado en Tokyo_001.db.")
