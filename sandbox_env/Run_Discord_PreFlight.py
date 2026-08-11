import os
from PreFlight_Core import PreFlightOrchestrator

if __name__ == "__main__":
    orquestador = PreFlightOrchestrator()
    with open(r"C:\NULOGIC_CORE\Trading\Conector_Discord.py", "r", encoding="utf-8") as f:
        codigo = f.read()
    # Forzar cambio de firma agregando un token de latido dinámico único
    codigo_dinamico = f"{codigo}\n# LATIDO_MUTADO_DISCORD = 181230\n"
    print("[*] Iniciando simulación definitiva en jaula de arena...")
    orquestador.validar_y_optimizar("Conector_Discord_Asincrono", codigo_dinamico)
