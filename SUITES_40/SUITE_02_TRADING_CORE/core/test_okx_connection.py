import ccxt, json

try:
    with open('okx_credentials.json', 'r', encoding='utf-8-sig') as f:
        config = json.load(f)
except Exception as e:
    print(f"[ERROR DE LECTURA JSON]: {e}")
    exit(1)

creds = config.get('credentials', {})
exchange = ccxt.okx({
    'apiKey': creds.get('api_key'),
    'secret': creds.get('secret_key'),
    'password': creds.get('passphrase'),
    'enableRateLimit': True,
    'options': {'defaultType': 'swap'}
})

try:
    balance = exchange.fetch_balance()
    print('\n--- ¡CONEXIÓN ESTABLECIDA CON ÉXITO! ---')
    total_usd = balance.get('total', {}).get('USDT', balance.get('total', {}).get('USD', '0'))
    print(f'Equivalente Total USD: ${total_usd}')
    
    print('\nSaldos disponibles:')
    for c, v in balance.get('free', {}).items():
        if v and float(v) > 0:
            print(f' -> {c}: {v}')
except Exception as e:
    print(f'\n[ERROR DE CONEXIÓN CON OKX]: {str(e)}')