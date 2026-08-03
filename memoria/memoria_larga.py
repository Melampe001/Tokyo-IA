# ============================================================
# memoria_larga.py - MEMORIA A LARGO PLAZO
# ============================================================
# QUE HACE: Guarda lo MÃS IMPORTANTE de forma permanente.
# No guarda todo, solo lo que vale la pena recordar siempre.
# Nunca se limpia sola, crece con el tiempo.
#
# EQUIVALENTE HUMANO: Lo que recuerdas de meses o aÃ±os.
# Tu cerebro no guarda todo, filtra lo importante.
#
# EJEMPLO DE LO QUE GUARDA:
#   - "Al usuario le interesa la programaciÃ³n y las terapias"
#   - "Prefiere explicaciones con ejemplos"
#   - "EstÃ¡ construyendo un sistema de habla para IA"
# ============================================================

import json

class MemoriaLarga:
    def __init__(self, archivo="memoria_permanente.json"):
        self.archivo = archivo

    def guardar_dato_importante(self, categoria, dato):
        """
        Guarda algo que siempre debe recordarse.
        categoria puede ser: 'preferencia', 'proyecto', 'personalidad'
        """
        pass

    def obtener_perfil_usuario(self):
        """Regresa todo lo que se sabe del usuario"""
        pass

    def decidir_si_guardar(self, texto):
        """
        FILTRO IMPORTANTE: Decide si algo vale la pena
        guardarse en memoria larga o no.
        No todo se guarda, igual que el cerebro humano.
        """
        pass
