# ============================================================
# memoria_mediana.py - MEMORIA A MEDIANO PLAZO
# ============================================================
# QUE HACE: Guarda conversaciones de los Ãºltimos dÃ­as.
# Persiste aunque cierres el chat.
# Se va reduciendo con el tiempo (resÃºmenes).
#
# EQUIVALENTE HUMANO: Lo que recuerdas de lo que
# platicaste ayer o antier.
#
# EJEMPLO DE LO QUE GUARDA:
#   - Resumen de la conversaciÃ³n del lunes
#   - Temas importantes de la semana
#   - Cosas que quedaron pendientes
# ============================================================

import json
from datetime import datetime, timedelta

class MemoriaMediana:
    def __init__(self, archivo="historial_reciente.json"):
        self.archivo = archivo
        self.dias_a_guardar = 7  # Guarda hasta 7 dÃ­as

    def guardar_sesion(self, resumen_sesion):
        """Guarda el resumen de una sesiÃ³n completa"""
        pass

    def obtener_sesiones_recientes(self, dias=3):
        """Regresa resÃºmenes de los Ãºltimos N dÃ­as"""
        pass

    def limpiar_antiguas(self):
        """Elimina conversaciones mÃ¡s viejas que el lÃ­mite"""
        pass
