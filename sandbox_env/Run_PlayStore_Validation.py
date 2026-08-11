from PreFlight_Core import PreFlightOrchestrator
import time

orquestador = PreFlightOrchestrator()
with open(r"C:\NULOGIC_CORE\Trading\Conector_SaaS_Pipeline.py", "r", encoding="utf-8") as f:
    codigo_original = f.read()

# Forzar una firma hash única para desarmar el bucle de la caché estática en el AST
token_dinamico = int(time.time())
codigo_mutado = f"{codigo_original}\n# GOOGLE_PLAY_MUTATION_TOKEN = {token_dinamico}\n"

print("[*] Iniciando simulación definitiva y empaquetado asíncrono...")
orquestador.validar_y_optimizar(f"Conector_SaaS_Pipeline_{token_dinamico}", codigo_mutado)
