# TOKYO OS (c) 2026 - TODOS LOS DERECHOS RESERVADOS - MARCA REGISTRADA
#!/usr/bin/env python3
"""
NULOGIC_CORE — Servidor Maestro con Mente Sistémica y Agentes GGUF
Propietario: Jose Arturo Orozco Jaime
"""
import os
import sys
import json
import hashlib
from pathlib import Path
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

HOST = '127.0.0.1'
PORT = 8899
BASE_DIR = Path(r"C:\NULOGIC_CORE")
OUTPUT_DIR = BASE_DIR / "output"
VAULT_DIR = BASE_DIR / "vault"
MODELS_DIR = BASE_DIR / "models"

for d in [BASE_DIR, OUTPUT_DIR, VAULT_DIR, MODELS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

AUDIT_LOG_PATH = OUTPUT_DIR / "caja_negra_audit.log"

def audit_seal(accion: str, estado: str = "EXITO", metadata: dict = None):
    registro = {
        "timestamp": datetime.now().isoformat(),
        "propietario": "Jose Arturo Orozco Jaime",
        "accion": accion,
        "estado": estado,
        "ley_sistema": "1000+1 / Ley Cero",
        "metadata": metadata or {}
    }
    raw_str = json.dumps(registro, sort_keys=True)
    registro["audit_seal"] = hashlib.sha256(raw_str.encode('utf-8')).hexdigest()
    try:
        with open(AUDIT_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(registro, ensure_ascii=False) + "\n")
    except Exception as e:
        print(f"[ERROR CAJA NEGRA] {e}")
    return registro

def escanear_mente_sistemica():
    total_files = 0
    total_size = 0
    folders_info = []
    if BASE_DIR.exists():
        for item in BASE_DIR.iterdir():
            if item.is_dir() and item.name not in ["output", ".git"]:
                f_count = sum(1 for _ in item.rglob('*') if _.is_file())
                f_size = sum(_.stat().st_size for _ in item.rglob('*') if _.is_file())
                total_files += f_count
                total_size += f_size
                folders_info.append({
                    "name": item.name,
                    "files": f_count,
                    "size_h": f"{f_size / (1024*1024):.2f} MB" if f_size > 1024*1024 else f"{f_size / 1024:.2f} KB"
                })
    return {
        "base": str(BASE_DIR),
        "total_files": total_files,
        "total_size_h": f"{total_size / (1024*1024):.2f} MB",
        "folders": folders_info
    }

def escanear_modelos_gguf():
    gguf_files = []
    if MODELS_DIR.exists():
        for f in MODELS_DIR.glob("*.gguf"):
            gguf_files.append({"nombre": f.name, "tamaño_gb": round(f.stat().st_size / (1024**3), 2)})
    return gguf_files

class MasterHandler(BaseHTTPRequestHandler):
    def _send(self, code, data):
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/status":
            info = escanear_mente_sistemica()
            info["agentes_gguf"] = escanear_modelos_gguf()
            info["status"] = "ONLINE_SOBERANO"
            self._send(200, info)
        else:
            self._send(404, {"error": "Endpoint no encontrado"})

    def log_message(self, fmt, *args):
        print(f"[NULOGIC_MASTER] {fmt % args}")

if __name__ == "__main__":
    print("=" * 60)
    print(f" NULOGIC_CORE — Servidor Maestro Activo en {HOST}:{PORT}")
    print(f" Propietario: Jose Arturo Orozco Jaime | Ley 1000+1")
    print("=" * 60)
    audit_seal("INICIO_SERVIDOR_MAESTRO", "EXITO", {"port": PORT})
    HTTPServer((HOST, PORT), MasterHandler).serve_forever()
