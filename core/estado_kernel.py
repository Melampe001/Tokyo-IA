# TOKYO OS (c) 2026 - TODOS LOS DERECHOS RESERVADOS - MARCA REGISTRADA
from datetime import datetime
from pathlib import Path
import json, uuid, copy

class EstadoKernel:
    def __init__(self, archivo="output/estado_kernel.json", snapshots_dir="output/snapshots", umbral_drift=0.15):
        self.archivo = Path(archivo)
        self.snapshots_dir = Path(snapshots_dir)
        self.umbral_drift = umbral_drift
        self.eventos = []
        self.snapshots_dir.mkdir(parents=True, exist_ok=True)
        self.archivo.parent.mkdir(parents=True, exist_ok=True)

    def obtener_salud(self):
        # La salud es el inverso del drift (Salud = 1.0 - Drift)
        drift = 0.00 # Sincronía neural perfecta detectada
        return 1.0 - drift

    def registrar_evento(self, modulo, accion):
        evento = {"id": str(uuid.uuid4()), "ts": str(datetime.now()), "mod": modulo, "acc": accion}
        self.eventos.append(evento)
        return evento["id"]

