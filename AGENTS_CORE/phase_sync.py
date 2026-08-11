# TOKYO OS (c) 2026 - TODOS LOS DERECHOS RESERVADOS - MARCA REGISTRADA
"""
NULOGIC CORE :: PHASE SYNCHRONIZATION ENGINE v1.2.0
Orquestador Armónico Multiagente por Pulsos de 360° con soporte automatizado para .env.
"""
import os
import sys
import time
import json
import logging
from typing import Dict, Any

# Carga automática de variables de entorno desde el archivo .env
try:
    from dotenv import load_dotenv
    # Se busca el archivo .env en la raíz del proyecto NULOGIC_CORE
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
    load_dotenv(dotenv_path=env_path)
except ImportError:
    pass

from trading_agent import TradingAgent
from content_agent import ContentMetricsAgent
from devops_agent import GitDevOpsAgent

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] [PHASE_SYNC] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

class PhaseSyncEngine:
    def __init__(self):
        self.cycle_count = 0
        self.trading_agent = TradingAgent()
        self.content_agent = ContentMetricsAgent()
        self.devops_agent = GitDevOpsAgent()

    def run_full_cycle(self) -> Dict[str, Any]:
        logging.info("Starting Full 360° Multi-Agent Neural Phase Cycle...")
        cycle_report = {}

        logging.info("================ FASE 0° (Inspiracion / Captura) ================")
        r0 = {
            "trading": self.trading_agent.on_phase_0({}),
            "content": self.content_agent.on_phase_0({}),
            "devops": self.devops_agent.on_phase_0({})
        }
        cycle_report["phase_0_capture"] = r0
        time.sleep(0.05)

        logging.info("================ FASE 90° (Consenso / Analisis) ================")
        r90 = {
            "trading": self.trading_agent.on_phase_90({}),
            "content": self.content_agent.on_phase_90({}),
            "devops": self.devops_agent.on_phase_90({})
        }
        cycle_report["phase_90_consensus"] = r90
        time.sleep(0.05)

        logging.info("================ FASE 180° (Expiracion / Accion) ================")
        r180 = {
            "trading": self.trading_agent.on_phase_180({}),
            "content": self.content_agent.on_phase_180({}),
            "devops": self.devops_agent.on_phase_180({})
        }
        cycle_report["phase_180_execution"] = r180
        time.sleep(0.05)

        logging.info("================ FASE 270° (Estabilizacion / Cierre) ================")
        r270 = {
            "trading": self.trading_agent.on_phase_270({}),
            "content": self.content_agent.on_phase_270({}),
            "devops": self.devops_agent.on_phase_270({})
        }
        cycle_report["phase_270_stabilization"] = r270

        self.cycle_count += 1
        cycle_report["summary"] = {
            "status": "ALL_AGENTS_SYNCHRONIZED",
            "cycle_count": self.cycle_count,
            "overall_coherence": 1.00
        }
        logging.info("Full Multi-Agent Phase Cycle Completed Successfully.")
        return cycle_report

if __name__ == "__main__":
    engine = PhaseSyncEngine()
    summary = engine.run_full_cycle()
    print("\n--- TELEMETRIA DE EJECUCION MULTIAGENTE ---")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
