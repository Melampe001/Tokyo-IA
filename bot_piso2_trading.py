import json, time, requests

print("\n[🚀] INICIANDO MOTOR DE TRADING AUTÓNOMO (PISO 2) - MONITOREO EN VIVO")

for i in range(3):
    try:
        url = "https://www.okx.com/api/v5/market/ticker?instId=BTC-USDT"
        response = requests.get(url, timeout=5).json()
        
        if response.get("code") == "0":
            precio_actual = float(response["data"][0]["last"])
            print(f"   📊 [MERCADO OKX] Precio BTC-USDT: ${precio_actual:,.2f}")
            
            umbral_compra = 65000.00
            if precio_actual < umbral_compra:
                print(f"   🟢 [ACCIÓN] Precio por debajo de {umbral_compra}. ¡Señal de COMPRA simulada!")
            else:
                print(f"   ⏳ [ACCIÓN] Precio actual en banda estable. Monitoreando volatilidad...")
        else:
            print(f"[⚠️] Respuesta de API OKX: {response.get('msg')}")
    except Exception as e:
        print(f"[❌] Error de conexión con OKX: {e}")
    
    time.sleep(2)

print("\n[✅] Ciclo de análisis de mercado ejecutado correctamente.")
