# TOKYO OS (c) 2026 - TODOS LOS DERECHOS RESERVADOS - MARCA REGISTRADA
import os
import sys
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

sys.path.append(os.path.dirname(__file__))
from license_db_manager import PRODUCTS_CATALOG, LicenseManager
from okx_signals_engine import OKXSignalsEngine

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

PAYMENT_LINKS = {
    "A": "https://buy.stripe.com/test_trading_bot_pro",
    "B": "https://buy.stripe.com/test_saas_boilerplate",
    "C": "https://buy.stripe.com/test_vip_membership",
    "D": "https://buy.stripe.com/test_devops_suite"
}

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "TU_TELEGRAM_BOT_TOKEN_AQUI")
db_manager = LicenseManager()
okx_engine = OKXSignalsEngine()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    welcome_text = (
        f"⚡ *¡Bienvenido a FlaggShip Apps & RascaCielos-Digital®!* ⚡\n\n"
        f"Hola {user_name}, soy el Bot Oficial de *Tokyo M.*\n"
        f"Usa este bot para comprar productos, consultar tus licencias o recibir señales de trading OKX.\n\n"
        f"📌 *Comandos Disponibles:*\n"
        f"• /catalogo - Ver productos y links de pago\n"
        f"• /validar <CLAVE> - Validar estado de tu licencia\n"
        f"• /senal <CLAVE> - Obtener última señal VIP de OKX\n"
    )
    await update.message.reply_text(welcome_text, parse_mode="Markdown")

async def catalogo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = []
    for key, prod in PRODUCTS_CATALOG.items():
        button = [InlineKeyboardButton(f"📦 {prod['name']} —  USD", callback_data=f"info_{key}")]
        keyboard.append(button)
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("⚡ *Catálogo Oficial FlaggShip Apps:*", parse_mode="Markdown", reply_markup=reply_markup)

async def validar_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ Uso correcto: /validar RASCACIELOS-XXXX-XXXX-XXXX", parse_mode="Markdown")
        return
    key = context.args[0]
    valid, details = db_manager.verify_license(key)
    if valid:
        text = f"✅ *Licencia Válida*\n\n📦 *Producto:* {details['product_name']}\n👤 *Cliente:* {details['customer_name']}\n📅 *Expira:* {details['expires_at']}"
    else:
        text = f"❌ *Error:* {details}"
    await update.message.reply_text(text, parse_mode="Markdown")

async def senal_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ Uso correcto: /senal RASCACIELOS-TRAD-XXXX-XXXX", parse_mode="Markdown")
        return
    key = context.args[0]
    result = okx_engine.generate_signal(key)
    if result.get("status") == "ERROR":
        await update.message.reply_text(f"🛑 {result.get('message')}")
    else:
        sig = result["signal"]
        text = (
            f"📈 *SEÑAL VIP OKX TRADING* 📈\n\n"
            f"🔹 *Par:* {sig['pair']}\n"
            f"🔹 *Acción:* {sig['action']}\n"
            f"🔹 *Entrada:* ${sig['entry']}\n"
            f"🎯 *Take Profit:* ${sig['take_profit']}\n"
            f"🛑 *Stop Loss:* ${sig['stop_loss']}\n"
            f"⚡ *Apalancamiento:* {sig['leverage']}"
        )
        await update.message.reply_text(text, parse_mode="Markdown")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    if data.startswith("info_"):
        product_key = data.split("_")[1]
        prod = PRODUCTS_CATALOG.get(product_key)
        pay_link = PAYMENT_LINKS.get(product_key, "#")
        info_text = (
            f"🎯 *{prod['name']}*\n\n"
            f"🔹 *ID:* {prod['id']} | *Precio:* ${prod['price']} USD\n"
            f"Haz clic abajo para pagar. Recibirás tu licencia por correo y en este chat."
        )
        keyboard = [
            [InlineKeyboardButton("💳 Pagar Ahora", url=pay_link)],
            [InlineKeyboardButton("⬅️ Volver", callback_data="back_catalog")]
        ]
        await query.edit_message_text(info_text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))
    elif data == "back_catalog":
        keyboard = [[InlineKeyboardButton(f"📦 {prod['name']} —  USD", callback_data=f"info_{key}")] for key, prod in PRODUCTS_CATALOG.items()]
        await query.edit_message_text("⚡ *Catálogo Oficial FlaggShip Apps:*", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

if __name__ == '__main__':
    if TELEGRAM_TOKEN != "TU_TELEGRAM_BOT_TOKEN_AQUI":
        app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("catalogo", catalogo))
        app.add_handler(CommandHandler("validar", validar_cmd))
        app.add_handler(CommandHandler("senal", senal_cmd))
        app.add_handler(CallbackQueryHandler(button_handler))
        print("[🚀 TELEGRAM BOT V24.5 LIVE] Servidor activo...")
        app.run_polling()
    else:
        print("[⚠️ ATENCIÓN] Configura TELEGRAM_BOT_TOKEN para encender el bot.")

