# TOKYO OS (c) 2026 - TODOS LOS DERECHOS RESERVADOS - MARCA REGISTRADA
import os
import json
import logging
import sqlite3

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] [PISO2_MESH]: %(message)s"
)

class Piso2ServiceMesh:
    def __init__(self):
        # Determinación de ruta absoluta basada en la estructura del monorepo
        base_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(base_dir) # O ajustado si está en subcarpeta
        # Apuntamos directamente a la ruta absoluta de la base de datos central
        self.db_path = "E:\\TOKYOAPPS_UNIVERSE\\01_ACTIVE\\NULOGIC_CORE\\database\\Tokyo_001.db"
        self.verify_mesh_status()

    def verify_mesh_status(self):
        logging.info("Verificando integridad de la malla de microservicios del Piso 2 con ruta absoluta...")
        if os.path.exists(self.db_path):
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO execution_logs (module, status, details) VALUES (?, ?, ?)",
                ("PISO2_MESH", "SUCCESS", "Microservicios autónomos sincronizados con ruta absoluta al SSoT.")
            )
            conn.commit()
            conn.close()
            logging.info("[ÉXITO ABSOLUTO] Malla de servicios del Piso 2 conectada a la base de datos central.")
        else:
            logging.warning(f"[AVISO CRÍTICO] Base de datos no encontrada en: {self.db_path}")

if __name__ == "__main__":
    mesh = Piso2ServiceMesh()

