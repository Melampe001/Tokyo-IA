# TOKYO OS (c) 2026 - TODOS LOS DERECHOS RESERVADOS - MARCA REGISTRADA
import os
from PreFlight_Core import PreFlightOrchestrator

if __name__ == "__main__":
    orquestador = PreFlightOrchestrator()
    ruta_archivo = r"C:\NULOGIC_CORE\sandbox_env\Módulo_Seguridad_Binance.py"
    
    with open(ruta_archivo, "r", encoding="utf-8") as f:
        codigo_nodo = f.read()
        
    print("\n[*] Lanzando simulación de contingencia sobre Módulo_Seguridad_Binance...")
    orquestador.validar_y_optimizar("Módulo_Seguridad_Binance", codigo_nodo)

