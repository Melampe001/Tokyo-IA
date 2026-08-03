# ==============================================================================
# FLAGGSHIP APPS - TRINITY ATOMIZED CONTAINER (2026)
# ==============================================================================
FROM python:3.11-slim

WORKDIR /app

# Copiar el motor y los módulos esenciales
COPY ./AGENTS_CORE /app/agents/
COPY ./SUITES_40 /app/suites/

# Instalar dependencias base de la Tríada y Cloud SDKs
RUN pip install --no-cache-dir azure-identity boto3 google-cloud-aiplatform requests

# Variables de entorno predeterminadas para el operador
ENV OPERATOR="Jose Arturo Orozco Jaime / Tokyo M."
ENV BRAND="FlaggShip Apps"
ENV VEHICLE="Zeekr 001 Flagship"

CMD ["python", "/app/suites/SUITE_01_COMMERCIAL_GATEWAY/billing_webhook.py"]
