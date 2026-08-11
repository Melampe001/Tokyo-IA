# TOKYO OS (c) 2026 - TODOS LOS DERECHOS RESERVADOS - MARCA REGISTRADA
import uvicorn

if __name__ == "__main__":
    print("=========================================================")
    print("🚀 INICIANDO RASCACIELOS DIGITAL ATOM - SERVIDOR 24/7")
    print("Propietario: Jose Arturo Orozco Jaime (TokyoApps)")
    print("=========================================================")
    uvicorn.run("app.main_production:app", host="0.0.0.0", port=8000, reload=False, workers=4)
