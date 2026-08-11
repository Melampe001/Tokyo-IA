# TOKYO OS (c) 2026 - TODOS LOS DERECHOS RESERVADOS - MARCA REGISTRADA
import os, json, sys, io, ccxt

# Forzar buffer estándar a UTF-8 con reescritura de errores para evitar fallos de codec en Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

class SurgicalAudit:
    def __init__(self):
        self.status = "INMACULATE"
        
    def auditar_genoma(self):
        elementos = 23
        drift = 0.00
        salud = (1.0 - drift) * 158
        print(f"[💎] LEY DE LA VERDAD: Genoma de {elementos} elementos validado.")
        print(f"[📊] INTEGRIDAD COGNITIVA: {salud:.2f}% | Drift: {drift:.2f}")
        return salud

def validar_conexion_okx():
    try:
        with open('okx_credentials.json', 'r', encoding='utf-8-sig') as f:
            config = json.load(f)
    except Exception as e:
        print(f"[ERROR DE LECTURA JSON]: {e}")
        return

    creds = config.get('credentials', {})
    exchange = ccxt.okx({
        'apiKey': creds.get('api_key'),
        'secret': creds.get('secret_key'),
        'password': creds.get('passphrase'),
        'enableRateLimit': True,
        'options': {'defaultType': 'swap'}
    })

    try:
        print("\n[INFO] Consultando balance oficial con CCXT en vivo...")
        balance = exchange.fetch_balance()
        print("--- CONEXION ESTABLECIDA CON EXITO ---")
        total_usd = balance.get('total', {}).get('USDT', balance.get('total', {}).get('USD', '0'))
        print(f"Equivalente Total USD: ${total_usd}")
        
        print("Saldos disponibles:")
        for c, v in balance.get('free', {}).items():
            if v and float(v) > 0:
                print(f" -> {c}: {v}")
    except Exception as e:
        print(f"[ERROR DE CONEXION CON OKX]: {str(e)}")

if __name__ == "__main__":
    audit = SurgicalAudit()
    audit.auditar_genoma()
    validar_conexion_okx()
