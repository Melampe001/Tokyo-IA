# TOKYO OS (c) 2026 - TODOS LOS DERECHOS RESERVADOS - MARCA REGISTRADA
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from services.resend_monetization_engine import RascacielosResendEngine

def process_live_trade_event(symbol, side, amount, profit_usdt):
    engine = RascacielosResendEngine()
    signal_data = {
        "symbol": symbol,
        "action": side,
        "size": amount,
        "profit": profit_usdt
    }
    vip_subscriber = os.getenv("VIP_SIGNAL_EMAIL", "vip@tokyoapps.io")
    result = engine.send_vip_trading_signal(vip_subscriber, signal_data)
    print(f"[📈 DISPARADOR OKX] Alerta procesada: {result['status']}")

if __name__ == "__main__":
    process_live_trade_event("BTC-USDT-SWAP", "BUY_ARBITRAGE", "0.05", "+12.45")

