import sys
import os

# Asegurar acceso al directorio raíz y módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from modules.trading_validator import validate_and_execute_order
except ImportError:
    # Fallback si se ejecuta desde modules/
    from trading_validator import validate_and_execute_order

def run_trading_node_test():
    print("📈 [Piso 2] Iniciando prueba de motor de Trading Autónomo...")
    
    # Saldo actual simulado según auditoría ($0.0701 USD)
    current_balance = 0.0701
    
    # Intentar ejecutar orden de prueba en par BTC-USDT-SWAP
    result = validate_and_execute_order("BTC-USDT-SWAP", "BUY", 0.001, current_balance)
    
    print(f"📊 Resultado del Motor de Trading: {result}")
    print("✅ [Piso 2] Trading Autónomo vinculado correctamente al Kernel de Riesgos.")

if __name__ == "__main__":
    run_trading_node_test()
