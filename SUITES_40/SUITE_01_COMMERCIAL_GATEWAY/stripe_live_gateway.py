# TOKYO OS (c) 2026 - TODOS LOS DERECHOS RESERVADOS - MARCA REGISTRADA
# ==============================================================================
# FLAGGSHIP APPS - LIVE STRIPE PAYMENT PROCESSOR (2026)
# ==============================================================================
import os
import stripe
from flask import Flask, jsonify, request

app = Flask(__name__)

# Configuración de llaves de producción (Se cargan desde las variables de entorno seguras de la Tríada)
stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_live_placeholder_key")
WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "whsec_placeholder_secret")

@app.route("/create-checkout-session", methods=["POST"])
def create_checkout_session():
    try:
        data = request.get_json()
        tier = data.get("tier", "tier_1_pro")
        
        # Precios mapeados para FlaggShip Apps (SaaS Model)
        prices = {
            "tier_1_pro": "price_pro_monthly_id",       # $49.99 USD
            "tier_2_enterprise": "price_enterprise_id"  # $199.99 USD
        }
        
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': prices.get(tier, prices["tier_1_pro"]),
                'quantity': 1,
            }],
            mode='subscription',
            success_url='https://flaggshipapps.com/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='https://flaggshipapps.com/cancel',
        )
        return jsonify({"checkout_url": checkout_session.url}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/webhook", methods=["POST"])
def stripe_webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get('Stripe-Signature')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, WEBHOOK_SECRET
        )
    except ValueError as e:
        return "Invalid payload", 400
    except stripe.error.SignatureVerificationError as e:
        return "Invalid signature", 400

    # Manejar el evento de pago exitoso en tiempo real
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print(f"[LIVE TRANSACTION SUCCESS] Cliente ID: {session.get('customer')} | Monto procesado en cuenta real.")
        # Aquí el sistema habilita automáticamente los accesos al usuario

    return jsonify(status="success"), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

