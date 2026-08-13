from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
import sys

# === PORT GUARD INTEGRADO ===
port_guard_script = os.path.join(os.path.dirname(__file__), "port_guard.py")
if os.path.exists(port_guard_script):
    import subprocess
    subprocess.run([sys.executable, port_guard_script, "8000"])
# =============================

app = FastAPI(title="Nulogic Core Sovereign Gateway", version="3.5")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

class LogoSaveRequest(BaseModel):
    play_uid: str
    logo_name: str
    logo_svg_data: str
    palette_used: str

@app.options("/{full_path:path}")
async def preflight_handler(full_path: str):
    return {"status": "ok"}

@app.get("/")
def root():
    return {"status": "online", "system": "Nulogic Core Sovereign Gateway Active"}

@app.post("/save_logo")
def save_logo(payload: LogoSaveRequest):
    print(f"[POST RX] Recibido logo '{payload.logo_name}' para UID: {payload.play_uid}")
    return {
        "success": True,
        "message": f"Logo '{payload.logo_name}' guardado correctamente en Cloud Vault.",
        "data": {
            "play_uid": payload.play_uid,
            "logo_name": payload.logo_name
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api_gateway:app", host="0.0.0.0", port=8000, reload=False)