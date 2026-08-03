import os, sys, time, json, io, ccxt

# Forzar codificación inmaculada
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def ejecutar_disparos_prueba():
    path_creds = r"E:\TOKYOAPPS_UNIVERSE\01_ACTIVE\NULOGIC_CORE\SUITES_40\SUITE_02_TRADING_CORE\okx_credentials.json"
    try:
        with open(path_creds, "r", encoding="utf-8-sig") as f:
            creds = json.load(f).get("credentials", {})
    except Exception as e:
        print(f"[❌ ERROR]: No se pudieron leer las credenciales: {e}")
        return

    exchange = ccxt.okx({
        'apiKey': creds.get("api_key"),
        'secret': creds.get("secret_key"),
        'password': creds.get("passphrase"),
        'enableRateLimit': True,
        'options': {'defaultType': 'swap'}
    })

    print("\n[🚀 ElaraAI®]: Verificando conectividad y libros de órdenes en OKX...")
    try:
        t_inicio = time.perf_counter()
        ticker = exchange.fetch_ticker('BTC/USDT:USDT')
        t_latencia = (time.perf_counter() - t_inicio) * 1000
        
        precio_btc = ticker['last']
        print(f"[✅] CONEXIÓN ESTABLECIDA. Ticker BTC/USDT: ")
        print(f"[⚡] Latencia de ida y vuelta con OKX: {t_latencia:.2f}ms")
        
        print("\n[🎯] Evaluando condiciones para 'Disparos de Prueba' (Modo Seguro)...")
        balance = exchange.fetch_balance()
        usdt_free = balance.get('free', {}).get('USDT', 0)
        print(f"[📊] Saldo USDT Libre disponible para operación: ")
        
        if float(usdt_free) <= 0:
            print("[⚠️ AVISO]: El balance libre en USDT es 0. El nodo opera en modo de lectura y análisis de mercado.")
            print("[💡 SUGERENCIA]: Para ejecutar disparos reales con capital, asegúrate de tener fondos en la cuenta de Perpetuos/Swap de OKX.")
        else:
            print("[🔥 ESTADO]: Cuenta fondeada. El sistema está listo para ráfagas automatizadas de ejecución.")

    except Exception as e:
        print(f"[❌ ERROR EN EL DISPARO]: {str(e)}")

if __name__ == "__main__":
    ejecutar_disparos_prueba()