import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from services.resend_monetization_engine import RascacielosResendEngine

def trigger_post_purchase_flow(customer_email, plan_name, generated_token):
    engine = RascacielosResendEngine()
    result = engine.send_saas_onboarding(customer_email, plan_name, generated_token)
    print(f"[💳 DISPARADOR SAAS] Onboarding enviado a {customer_email}: {result['status']}")

if __name__ == "__main__":
    # Destinatario cambiado a tu correo de cuenta para pasar la validación 403 de Resend
    target_email = os.getenv("VIP_SIGNAL_EMAIL", "thenewtokyocompany@gmail.com")
    trigger_post_purchase_flow(target_email, "FlaggShip Premium Suite", "TK-88392-X")
