# TOKYO OS (c) 2026 - TODOS LOS DERECHOS RESERVADOS - MARCA REGISTRADA
import sys
import os
import importlib
import logging

def cargar_bloque_en_caliente(nombre_bloque):
    """Importa o recarga dinámicamente un módulo empaquetado en core."""
    ruta_core = r"C:\NULOGIC_CORE\core"
    if ruta_core not in sys.path:
        sys.path.append(ruta_core)
        
    try:
        if nombre_bloque in sys.modules:
            logging.info(f"[NÚCLEO] Recargando módulo existente: {nombre_bloque}")
            modulo = importlib.reload(sys.modules[nombre_bloque])
        else:
            logging.info(f"[NÚCLEO] Importando nuevo bloque al rascacielos: {nombre_bloque}")
            modulo = importlib.import_module(nombre_bloque)
            
        # Ejecución del punto de entrada estándar si existe
        if hasattr(modulo, 'liquidacion_nodos_emergencia'):
            modulo.liquidacion_nodos_emergencia()
        return True
    except Exception as e:
        logging.error(f"[CRÍTICO] Error al acoplar el bloque {nombre_bloque} en caliente: {e}")
        return False

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')
    # Prueba de acoplamiento del nuevo bloque empaquetado
    cargar_bloque_en_caliente("Modulo_Liquidacion_Emergencia")

