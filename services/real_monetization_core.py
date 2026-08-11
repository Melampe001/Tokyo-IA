# TOKYO OS (c) 2026 - TODOS LOS DERECHOS RESERVADOS - MARCA REGISTRADA
import os
import json
import urllib.request
import urllib.error
from license_db_manager import LicenseManager, PRODUCTS_CATALOG

class NulogicMonetizationEngine:
    def __init__(self):
        self.api_key = os.getenv("RESEND_API_KEY", "os.getenv('RESEND_API_KEY', 'ENV_NOT_SET')")
        self.from_email = os.getenv("RESEND_FROM_EMAIL", "TokyoApps <onboarding@resend.dev>")
        self.api_url = "https://api.resend.com/emails"
        self.db = LicenseManager()

    def deliver_product(self, product_key, customer_email, customer_name="Tokyo M."):
        license_key, prod = self.db.generate_product_license(product_key, customer_name, customer_email)
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) NULOGIC_CORE/1.0"
        }

        html_template = f"""
        <div style="font-family: Arial, sans-serif; background-color: #0f172a; color: #f8fafc; padding: 30px; border-radius: 10px;">
            <h1 style="color: #38bdf8; text-align: center;">⚡ RascaCielos-Digital® - ENTREGA DE PRODUCTO</h1>
            <p>¡Hola <strong>{customer_name}</strong>!</p>
            <p>Tu compra de <strong>{prod['name']}</strong> ha sido procesada correctamente.</p>
            
            <div style="background-color: #1e293b; padding: 20px; border-left: 4px solid #38bdf8; border-radius: 5px; margin: 20px 0;">
                <p style="margin: 5px 0;"><strong>Producto ID:</strong> {prod['id']}</p>
                <p style="margin: 5px 0;"><strong>Precio:</strong>  USD</p>
                <p style="margin: 5px 0;"><strong>Clave de Licencia VIP:</strong> <code style="background-color: #0f172a; padding: 4px 8px; color: #4ade80;">{license_key}</code></p>
            </div>

            <p style="font-size: 13px; color: #cbd5e1;">Guarda esta clave para activar tu acceso o consultar la API de verificación de NULOGIC_CORE.</p>
            <hr style="border-color: #334155; margin-top: 30px;">
            <p style="font-size: 12px; color: #94a3b8; text-align: center;">RascaCielos-Digital® — NULOGIC_CORE Engine v24.0 | Firmado por Tokyo M.</p>
        </div>
        """

        payload = {
            "from": self.from_email,
            "to": [customer_email],
            "subject": f"📦 [Entrega Instantánea] {prod['name']}",
            "html": html_template
        }

        try:
            req = urllib.request.Request(self.api_url, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')
            with urllib.request.urlopen(req) as resp:
                res = json.loads(resp.read().decode('utf-8'))
                print(f"[💰 ENTREGA PROCESADA] {prod['name']} -> {customer_email} | Licencia: {license_key}")
                return True, license_key
        except Exception as e:
            print(f"[❌ ERROR ENTREGA]: {str(e)}")
            return False, license_key

