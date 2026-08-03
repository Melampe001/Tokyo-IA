#!/bin/bash
# ==============================================================================
# 🛰️ SERVIDOR VPS CLOUD: SCRIPT DE INSTALACIÓN AUTOMÁTICA EN TIEMPO REAL
# MARCA: TokyoApps™ Technologics Global | DISPARADOR INDUSTRIAL LINUX
# ARCHITECT: José Arturo Orozco Jaime (Melampe001) | thenewtokyocompany@gmail.com
# ==============================================================================

echo "🪐 [TokyoAI™] Iniciando aprovisionamiento del servidor Linux VPS Cloud 24/7..."
echo "=============================================================================="

# 1. Configurar los DNS de Google nativos en Linux para evitar bloqueos del API de OKX
echo "⚙️ Configurando resolvedores DNS de alta disponibilidad (8.8.8.8)..."
sudo sed -i 's/#DNS=/DNS=8.8.8.8 8.8.4.4/g' /etc/systemd/resolved.conf
sudo systemctl restart systemd-resolved

# 2. Actualizar paquetes e instalar el motor Docker en el servidor
echo "📦 Instalando Docker y Docker Compose de grado de producción..."
sudo apt-get update -y && sudo apt-get upgrade -y
sudo apt-get install -y docker.io docker-compose git python3-pip

# 3. Clonar la fuente única de verdad (SSoT) de José Arturo Orozco Jaime desde GitHub
echo "📡 Descargando repositorio inmutable desde GitHub..."
if [ ! -d "/app/NULOGIC_CORE" ]; then
    git clone git@github.com:Melampe001/TokyoApps-Multispace-IA.git /app/NULOGIC_CORE
fi

cd /app/NULOGIC_CORE

# 4. Encender el clúster de microservicios distribuidos (ElaraAI™, Redis Cache y PostgreSQL)
echo "🚀 Lanzando contenedores en la nube con disponibilidad del 99.99%..."
sudo docker-compose up -d --build

echo "=============================================================================="
echo "🏁 ¡DESPLIEGUE FINALIZADO! Servidor de TokyoApps™ en línea las 24/7/365."
echo "=============================================================================="