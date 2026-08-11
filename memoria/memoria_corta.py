# TOKYO OS (c) 2026 - TODOS LOS DERECHOS RESERVADOS - MARCA REGISTRADA
import json
import os

class MemoriaCorta:
    def __init__(self, archivo='memoria/estado_persistente.json'):
        self.archivo = archivo
        self.historial = self.cargar_datos()

    def cargar_datos(self):
        if os.path.exists(self.archivo):
            with open(self.archivo, 'r') as f:
                return json.load(f)
        return {"estado_id": 0, "turnos": []}

    def obtener_ultimos(self, n=5):
        # Aseguramos que siempre devuelva una lista
        return self.historial.get("turnos", [])[-n:]

    def guardar_turno(self, usuario, respuesta):
        self.historial["estado_id"] += 1
        self.historial["turnos"].append({"usuario": usuario, "ia": respuesta})
        with open(self.archivo, 'w') as f:
            json.dump(self.historial, f, indent=4)

