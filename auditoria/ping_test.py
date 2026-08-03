# -*- coding: utf-8 -*-
import sys
import os
import time

# Forzar el reconocimiento de la ruta raíz en el sistema
sys.path.append('C:\\TOKYOAPPS-UNIVERSE')

from respuesta.generador import generar_respuesta

def realizar_ping():
    inicio = time.perf_counter()
    resultado = generar_respuesta("estado", None, None)
    fin = time.perf_counter()
    latencia = (fin - inicio) * 1000
    return f"NODE:0x454C415241 | LATENCY:{latencia:.2f}ms | STATUS:0x03"

if __name__ == '__main__':
    print(realizar_ping())