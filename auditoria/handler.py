# -*- coding: utf-8 -*-
import datetime
import pickle

def registrar_error_binario(excepcion, traza):
    log_data = {
        'timestamp': datetime.datetime.now(),
        'error': str(excepcion),
        'trace': str(traza)
    }
    # Volcado binario para auditoría de bajo nivel
    with open('C:\\TOKYOAPPS-UNIVERSE\\auditoria\\error_log.bin', 'ab') as f:
        pickle.dump(log_data, f)

# Integración en el generador.py (reemplazo de lógica)