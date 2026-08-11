import http.server
import socketserver
import sqlite3
import os

PORT = 8000
DB_PATH = "Tokyo_001.db"

class ArtifactDashboardHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/status":
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            
            logs = []
            try:
                if os.path.exists(DB_PATH):
                    conn = sqlite3.connect(DB_PATH)
                    cursor = conn.cursor()
                    cursor.execute("SELECT timestamp, module, message, status FROM system_logs ORDER BY id DESC LIMIT 15")
                    logs = cursor.fetchall()
                    conn.close()
            except:
                pass

            html = f"""
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <title>NULOGIC CORE - Sovereign Artifact Dashboard</title>
                <meta http-equiv="refresh" content="5">
                <style>
                    body {{ background-color: #0b0f19; color: #00ffcc; font-family: 'Courier New', monospace; padding: 20px; }}
                    h1 {{ border-bottom: 2px solid #00ffcc; padding-bottom: 10px; }}
                    .card {{ background: #111827; border: 1px solid #1f2937; padding: 15px; margin-bottom: 15px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }}
                    table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
                    th, td {{ border: 1px solid #374151; padding: 8px; text-align: left; font-size: 14px; }}
                    th {{ background: #1f2937; color: #fff; }}
                    .SUCCESS {{ color: #10b981; }}
                    .WARNING {{ color: #f59e0b; }}
                    .ERROR {{ color: #ef4444; }}
                </style>
            </head>
            <body>
                <h1>🛡️ NULOGIC CORE // SOBERANO 24/7</h1>
                <div class="card">
                    <h3>Estado del Sistema: <span style="color: #10b981;">ONLINE (Military-Grade Secure)</span></h3>
                    <p>Ubicación Activa: <strong>E:/TOKYOAPPS_UNIVERSE/01_ACTIVE/NULOGIC_CORE</strong></p>
                    <p>Espejo de Respaldo: <strong>C:/NULOGIC_MIRROR</strong></p>
                </div>
                <div class="card">
                    <h3>Artefactos y Telemetría en Tiempo Real</h3>
                    <table>
                        <tr><th>Timestamp</th><th>Módulo</th><th>Mensaje</th><th>Estado</th></tr>
            """
            for row in logs:
                status_class = row[3]
                html += f"<tr><td>{row[0]}</td><td><strong>{row[1]}</strong></td><td>{row[2]}</td><td class='{status_class}'>{row[3]}</td></tr>"
            
            html += """
                    </table>
                </div>
            </body>
            </html>
            """
            self.wfile.write(html.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

def run_dashboard():
    try:
        with socketserver.TCPServer(("", PORT), ArtifactDashboardHandler) as httpd:
            print(f"   🌐 [LOCALHOST DASHBOARD] Activo en http://127.0.0.1:{PORT}")
            httpd.serve_forever()
    except Exception as e:
        print(f"   ⚠️ [DASHBOARD ERROR] {e}")