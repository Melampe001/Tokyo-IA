@echo off
title Rascacielos Digital Atom - NEXUS-1 Live Core
color 0E
echo ==========================================================
echo INICIANDO RASCACIELOS DIGITAL ATOM (PRODUCCION 24/7)
echo Propietario: Jose Arturo Orozco Jaime (TokyoApps)
echo ==========================================================
cd /d E:\TOKYOAPPS_UNIVERSE\01_ACTIVE\NULOGIC_CORE\ATOM_MASTER_CORE
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
pause
