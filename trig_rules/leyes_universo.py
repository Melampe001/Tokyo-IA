import math
import random

class EvaluadorEvolutivoHFT:
    @staticmethod
    def simular_estres_nodos() -> dict:
        """Inyecta fluctuaciones masivas de red y spreads para entrenar a TokyoAI™."""
        latencia_simulada = random.uniform(0.1, 1.8) # Latencia en ms
        spread_volatil = random.uniform(-2.5, 8.4)  # Spread simulado
        return {
            "ping": f"{round(latencia_simulada, 2)} ms",
            "spread": f"{round(spread_volatil, 4)}%",
            "score_concurrencia": random.randint(1000, 5000)
        }

    @staticmethod
    def verificar_coseno_fuentes(vector_actual: list, vector_maestro: list) -> float:
        """Calcula la similitud semántica contra las fuentes (NotebookLM API)."""
        producto_punto = sum(a * b for a, b in zip(vector_actual, vector_maestro))
        norma_a = math.sqrt(sum(a ** 2 for a in vector_actual))
        norma_b = math.sqrt(sum(b ** 2 for b in vector_maestro))
        if norma_a == 0 or norma_b == 0: return 0.0
        return producto_punto / (norma_a * norma_b)
