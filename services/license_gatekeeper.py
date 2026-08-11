# TOKYO OS (c) 2026 - TODOS LOS DERECHOS RESERVADOS - MARCA REGISTRADA
import os
from license_db_manager import LicenseManager

class FlaggShipGatekeeper:
    def __init__(self):
        self.db = LicenseManager()

    def validate_remote_client(self, api_token: str, license_key: str):
        # Validación de seguridad de token dev
        is_valid, details = self.db.verify_license(license_key)
        if not is_valid:
            return {"authorized": False, "reason": details}

        return {
            "authorized": True,
            "license_key": license_key,
            "product_code": details.get("product_code"),
            "product_name": details.get("product_name"),
            "expires_at": details.get("expires_at"),
            "status": details.get("status")
        }

