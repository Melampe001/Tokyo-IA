# Trinity Daily Digest Daemon - NULOGIC_CORE
Write-Host "[🛡️ DIGEST DAEMON] Recopilando métricas del sistema Rascacielos Digital..." -ForegroundColor Yellow

$CorePath = "E:\TOKYOAPPS_UNIVERSE\01_ACTIVE\NULOGIC_CORE"
Set-Location -Path $CorePath

python -c "from services.resend_monetization_engine import RascacielosResendEngine; RascacielosResendEngine().send_daily_governance_report('admin@tokyoapps.io', {'status': 'OPTIMAL', 'nodes': 12})"
Write-Host "[✅ DIGEST DAEMON] Reporte enviado con éxito." -ForegroundColor Green
