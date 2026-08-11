import os
from PreFlight_Core import PreFlightOrchestrator

if __name__ == "__main__":
    orquestador = PreFlightOrchestrator()
    ruta_conector = r"C:\NULOGIC_CORE\Trading\Conector_Binance.py"
    
    if os.path.exists(ruta_conector):
        with open(ruta_conector, "r", encoding="utf-8") as f:
            codigo_trading = f.read()
        print("\n[*] Iniciando simulación estática y empaquetado dinámico...")
        orquestador.validar_y_optimizar("Conector_Binance", codigo_trading)
