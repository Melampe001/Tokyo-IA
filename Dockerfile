# ===========================================================
# RascacielosDigital_UniverseAtom® :: DOCKERFILE OPTIMIZADO
# ===========================================================
FROM python:3.11-slim AS base

# Variables de entorno para Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app

WORKDIR /app

# Instalar dependencias del sistema requeridas
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente
COPY AGENTS_CORE /app/AGENTS_CORE
COPY .env.example /app/.env.example

# Diagnóstico de Salud interno del Contenedor
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request, os; exit(0 if os.path.exists('AGENTS_CORE/phase_sync.py') else 1)"

# Comando por defecto: Ejecutar el orquestador PhaseSync
CMD ["python", "AGENTS_CORE/phase_sync.py"]