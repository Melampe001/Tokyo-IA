# Standard Enterprise Base Image para aplicaciones híbridas de IA y Trading
FROM python:3.12-slim

# Definir variables de entorno de producción inmunes al colapso entrópico
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV ENVIRONMENT=production

WORKDIR /app

# Instalar dependencias del sistema requeridas para alta concurrencia
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Copiar manifiestos de dependencias e instalar con optimización de caché
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copiar la suite completa (Nucleo, Memoria, Interfaces TypeScript)
COPY . .

EXPOSE 8080

print("🔒 [TokyoAI] Contenedor de producción inicializado con éxito.")
CMD ["python", "main.py"]
