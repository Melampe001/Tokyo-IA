import os
import shutil
import logging

def transferir_a_produccion(nombre_bloque):
    origen = os.path.join(r"C:\NULOGIC_CORE\sandbox_env", f"{nombre_bloque}.py")
    destino = os.path.join(r"C:\NULOGIC_CORE\core", f"{nombre_bloque}.py")
    
    if os.path.exists(origen):
        shutil.copy2(origen, destino)
        logging.info(f"[PUENTE] Bloque '{nombre_bloque}' transferido con éxito a Producción.")
        return True
    return False
