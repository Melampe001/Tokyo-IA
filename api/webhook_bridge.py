from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        print(f"[📥] Webhook recibido: {body.decode('utf-8')}")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'{"status": "received"}')

def run(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, WebhookHandler)
    print(f"[🌐] Webhook Bridge escuchando en el puerto {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
