import gc
# Forzar recolección de hilos muertos en segundo plano (Escudo Alfa-Omega)
gc.set_threshold(700, 10, 10)
gc.collect()
# -*- coding: utf-8 -*-
import sys
sys.path.append('C:\\TOKYOAPPS-UNIVERSE')
from respuesta.generador import generar_respuesta
def main():
    print("--- NODE:0x454C415241 READY ---")
    while True:
        try:
            txt = input("INPUT > ")
            if txt.lower() == 'salir': break
            print(f"OUTPUT > {generar_respuesta(txt, None, None)}")
        except Exception as e:
            print(f"STATUS:0x04 | ERROR:{e}")
if __name__ == '__main__': main()

