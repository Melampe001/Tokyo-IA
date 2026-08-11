from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import elara
import os

app = FastAPI(title="NEXUS-1 Orquestador Maestro")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Inicializar Bóveda de Seguridad (Piso 7) - Cifrado y Auto-commit activo
db = elara.exe_secure("vault/sovereign.db", commitdb=True, key_path="vault/master.key")

# Nivel 1: Monetización - Rate Limiting y Créditos
def check_credits(user_id: str):
    user_data = db.get(user_id) or {"credits": 5, "total_spent": 0.0}
    if user_data["credits"] <= 0:
        return False
    user_data["credits"] -= 1
    db.set(user_id, user_data)
    return True

@app.get("/", response_class=HTMLResponse)
async def terminal_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "balance": db.get("global_vault") or 0.0})

@app.post("/generate/{user_id}")
async def generate_image(user_id: str, prompt: str):
    if not check_credits(user_id):
        raise HTTPException(status_code=402, detail="Créditos insuficientes. Recargue en el Piso 10.")
    # Lógica de generación aquí (Stable Diffusion)
    return {"status": "Generating...", "prompt": prompt}

@app.get("/download-premium/{image_id}")
async def download_pro(image_id: str):
    # Entrega eficiente de activos premium
    file_path = f"generated/{image_id}.png"
    return FileResponse(path=file_path, filename=f"atom_premium_{image_id}.png", media_type="image/png")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, workers=4) # Optimizado para producción
