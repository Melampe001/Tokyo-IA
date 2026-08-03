import datetime

class EstadoKernel:
    def __init__(self, umbral_drift=0.30):
        self.umbral_drift = umbral_drift
        self.eventos = []
        self.status = "INMACULADO"
        print(f"🔒 [Kernel Soberano] Inicializado con umbral_drift de {umbral_drift}")
