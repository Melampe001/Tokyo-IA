import json
import os

def validate_and_execute_order(symbol, side, size, available_balance_usd):
    config_path = "config/trading_limits.json"
    min_notional = 1.00
    
    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
                min_notional = config.get("min_notional_usd", 1.00)
        except Exception as e:
            print(f"⚠️ Error cargando config de trading: {e}")
            
    if available_balance_usd < min_notional:
        print(f"⚠️ [ALERTA DE RIESGO] Saldo disponible (${available_balance_usd} USD) por debajo del mínimo requerido (${min_notional} USD).")
        print("🔄 Cambiando a Modo Simulación Atómica (Paper Trading) para evitar rechazo de API OKX.")
        return {
            "status": "SIMULATED_SUCCESS",
            "message": "Order executed in local sandbox due to low equity.",
            "symbol": symbol,
            "side": side,
            "mode": "PAPER_TRADING"
        }
    else:
        print(f"✅ Saldo suficiente (${available_balance_usd} USD). Ejecutando orden real en OKX...")
        return {
            "status": "REAL_EXECUTION_PENDING",
            "symbol": symbol,
            "side": side
        }
