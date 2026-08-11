# TOKYO OS (c) 2026 - TODOS LOS DERECHOS RESERVADOS - MARCA REGISTRADA
import ccxt, json, os, sys, io
# SSSoT: Alineación de Rutas
sys.path.append(r"E:\TOKYOAPPS_UNIVERSE\01_ACTIVE\NULOGIC_CORE")
from core.estado_kernel import EstadoKernel

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def auditar_saldo_real():
    k = EstadoKernel()
    path_creds = r"E:\TOKYOAPPS_UNIVERSE\01_ACTIVE\NULOGIC_CORE\SUITES_40\SUITE_02_TRADING_CORE\okx_credentials.json"
    
    with open(path_creds, "r", encoding="utf-8-sig") as f:
        creds = json.load(f).get("credentials", {})
    
    # [🚀] CONFIGURACIÓN SOBERANA OKX
    exchange = ccxt.okx({
        'apiKey': creds.get("api_key"),
        'secret': creds.get("secret_key"),
        'password': creds.get("passphrase"),
        'enableRateLimit': True,
        'options': {'adjustForTimeDifference': True}
    })

    try:
        # [🎯] EXTRACCIÓN DE BALANCE (TRADING ACCOUNT)
        balance = exchange.fetch_balance()
        total_usdt = balance.get('USDT', {}).get('total', 0)
        total_btc = balance.get('BTC', {}).get('total', 0)
        
        print(f"\n[✅] HANDSHAKE EXITOSO: APIs y Phrase validadas al 100%.")
        print(f"[💰] SALDO DISPONIBLE (USDT): {total_usdt}")
        print(f"[💰] SALDO DISPONIBLE (BTC): {total_btc}")
        
        # Registro en el Kernel para Trazabilidad Reversible <RR>
        k.registrar_evento('FINANZAS', f'AUDITORIA_SALDO: USDT:{total_usdt} | BTC:{total_btc}')
        
    except Exception as e:
        print(f"[❌] FRICCIÓN DE AUTENTICACIÓN: Verifique su Phrase y APIs. Detalle: {str(e)}")

if __name__ == "__main__":
    auditar_saldo_real()

