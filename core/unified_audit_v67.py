import ccxt, json, os, sys, io
sys.path.append(r"E:\TOKYOAPPS_UNIVERSE\01_ACTIVE\NULOGIC_CORE")
from core.estado_kernel import EstadoKernel

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def ejecutar_auditoria_total(ip_detectada):
    k = EstadoKernel()
    # [💎] SUTURA DE SINTAXIS: IPv6 como string inmutable
    ip_error_reportada = "2806:261:b400:87a8:a137:4097:b5ea:66ec"
    
    print(f"\n[💎] LEY DE LA VERDAD: Validando IP de Silicio...")
    
    path_creds = r"E:\TOKYOAPPS_UNIVERSE\01_ACTIVE\NULOGIC_CORE\SUITES_40\SUITE_02_TRADING_CORE\okx_credentials.json"
    with open(path_creds, "r", encoding="utf-8-sig") as f:
        creds = json.load(f).get("credentials", {})

    # [🚀] CONFIGURACIÓN OKX v5
    exchange = ccxt.okx({
        'apiKey': creds.get("api_key"),
        'secret': creds.get("secret_key"),
        'password': creds.get("passphrase"),
        'enableRateLimit': True,
        'options': {'adjustForTimeDifference': True}
    })

    try:
        # Intento de Handshake de Saldo
        balance = exchange.fetch_balance()
        total_usdt = balance.get('USDT', {}).get('total', 0)
        
        print(f"[✅] SINCRO-IP EXITOSA: Red autorizada y operativa.")
        print(f"[💰] SALDO REAL OKX (USDT): {total_usdt}")
        k.registrar_evento('FINANZAS', f'SALDO_VALIDADO: {total_usdt} USDT')
        
    except Exception as e:
        if "50110" in str(e):
            print(f"[⚠️] BLOQUEO DE SEGURIDAD (50110):")
            print(f"    La IP {ip_detectada} NO está en la Whitelist de OKX.")
            print(f"    Acción: Agréguela en Perfil -> API -> Whitelist de IP.")
        else:
            print(f"[❌] FRICCIÓN OPERATIVA: {str(e)}")

if __name__ == "__main__":
    ejecutar_auditoria_total("2806:261:b400:87a8:a137:4097:b5ea:66ec")
