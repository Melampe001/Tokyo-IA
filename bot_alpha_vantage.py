# TOKYO OS (c) 2026 - TODOS LOS DERECHOS RESERVADOS - MARCA REGISTRADA
import json, time, requests

print("\n[🚀] INICIANDO MOTOR MULTI-FUENTE (OKX + ALPHA VANTAGE)")

# Intentar cargar Alpha Vantage API Key si está configurada
alpha_key = "demo"
try:
    with open("alpha_credentials.json", "r") as f:
        data = json.load(f)
        alpha_key = data.get("alpha_vantage", {}).get("api_key", "demo")
except:
    pass

for i in range(2):
    try:
        # 1. Consulta OKX (Cripto en vivo)
        url_okx = "https://www.okx.com/api/v5/market/ticker?instId=BTC-USDT"
        res_okx = requests.get(url_okx, timeout=5).json()
        if res_okx.get("code") == "0":
            precio_btc = float(res_okx["data"][0]["last"])
            print(f"   📊 [OKX - Cripto] BTC-USDT: ${precio_btc:,.2f}")

        # 2. Consulta Alpha Vantage (Forex / Acciones / Indicadores globales)
        # Usamos función GLOBAL_QUOTE para una acción de prueba o divisa si hay clave real
        url_av = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=IBM&apikey={alpha_key}"
        res_av = requests.get(url_av, timeout=5).json()
        
        if "Global Quote" in res_av and res_av["Global Quote"]:
            quote = res_av["Global Quote"]
            symbol = quote.get("01. symbol")
            price = quote.get("05. price")
            print(f"   📈 [Alpha Vantage] {symbol} Precio Global: ${price}")
        else:
            print(f"   ℹ️ [Alpha Vantage] Conectado (Usando modo DEMO/Llave de prueba)")

    except Exception as e:
        print(f"[❌] Error en consulta multi-fuente: {e}")
    
    time.sleep(2)

print("\n[✅] Sincronización multi-fuente completada.")

