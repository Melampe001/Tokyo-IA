from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

class DashboardHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = """
            <html>
                <head><title>NULOGIC_CORE Dashboard</title></head>
                <body style="background:#111; color:#0f0; font-family:monospace; padding:20px;">
                    <h1>[⚡] NULOGIC_CORE DASHBOARD</h1>
                    <p>Estado del Rascacielos Digital: ONLINE</p>
                    <hr>
                    <p>Servidor Maestro: ACTIVO</p>
                    <p>Watchdog Sonar: MONITORIZANDO</p>
                </body>
            </html>
            """
            self.wfile.write(html.encode('utf-8'))
        else:
            super().do_GET()

if __name__ == "__main__":
    server = HTTPServer(('localhost', 8501), DashboardHandler)
    print("[📊] Dashboard Web Activo en http://localhost:8501")
    server.serve_forever()
