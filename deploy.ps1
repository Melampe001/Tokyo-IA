# deploy.ps1 - Despliegue de Producción para RascacielosDigital
$ErrorActionPreference = "Stop"

Write-Host "🚀 Iniciando Despliegue de Producción RascacielosDigital..." -ForegroundColor Green

# 1. Ejecutar Suite de Salud Previa
Write-Host "🩺 Ejecutando Health Check Pre-Despliegue..." -ForegroundColor Yellow
node index.js --health-check

# 2. Construir Imagen Docker
Write-Host "📦 Construyendo imagen Docker (rascacielos-digital:latest)..." -ForegroundColor Yellow
docker build -t rascacielos-digital:latest .

# 3. Reiniciar Contenedor de Producción
Write-Host "🔄 Reiniciando servicio en contenedor..." -ForegroundColor Yellow
docker stop rascacielos-digital-prod -ErrorAction SilentlyContinue
docker rm rascacielos-digital-prod -ErrorAction SilentlyContinue
docker run -d --name rascacielos-digital-prod -p 3000:3000 --env-file .env.local rascacielos-digital:latest

# 4. Post-Deployment Health Check
Start-Sleep -Seconds 3
Write-Host "🏥 Ejecutando Verification Check en Vivo..." -ForegroundColor Cyan
node agents/deploy-agent.js --verify

Write-Host "🎉 DESPLIEGUE A PRODUCCIÓN COMPLETADO CON ÉXITO AL 100%" -ForegroundColor Green
