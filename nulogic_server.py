#!/usr/bin/env python3
"""
NULOGIC_CORE — Servidor local real
Propietario: Jose Arturo Orozco Jaime
"""
import os
import json
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

BASE_DIR = Path(r"C:\NULOGIC_CORE")
PORT = 8899

def get_status():
    status = {"base": str(BASE_DIR), "status": "ONLINE", "folders": []}
    if BASE_DIR.exists():
        for item in BASE_DIR.iterdir():
            if item.is_dir() and item.name not in ["output", ".git"]:
                files_count = sum(1 for _ in item.rglob('*') if _.is_file())
                status["folders"].append({"name": item.name, "files": files_count})
    return status

class ServerHandler(BaseHTTPRequestHandler):
    def _send(self, code, data):
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/health":
            self._send(200, {"ok": True, "base": str(BASE_DIR)})
        elif parsed.path == "/api/status":
            self._send(200, get_status())
        else:
            self._send(404, {"error": "endpoint no encontrado"})

    def log_message(self, fmt, *args):
        print(f"[NULOGIC_SERVER] {fmt % args}")

if __name__ == "__main__":
    print("=" * 60)
    print(" NULOGIC_CORE — Servidor local en ejecución")
    print(f" Escuchando en: http://127.0.0.1:{PORT}")
    print("=" * 60)
    server = HTTPServer(("127.0.0.1", PORT), ServerHandler)
    server.serve_forever()