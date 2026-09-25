import os
import subprocess
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import pyautogui

# --- CONFIGURACIÓN DE SEGURIDAD ---
TOKEN = "TOKEN_DEL_BOT_AQUI"
ADMIN_ID =  1234567890  # Reemplaza con tu ID numérico de Telegram

# Desactivar la pausa de seguridad de PyAutoGUI para respuestas rápidas
pyautogui.PAUSE = 0.1

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Verificación de usuario autorizado
def is_admin(update: Update) -> bool:
    return update.effective_user.id == ADMIN_ID

# Comando /start que despliega el teclado virtual en Telegram
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update):
        await update.message.reply_text("❌ No estás autorizado para controlar esta PC.")
        return

    # Diseño del menú de botones en Telegram
    keyboard = [
        ["🎵 Vol-", "🎵 Vol+", "⏯️ Play/Pausa"],
        ["⏮️ Anterior", "⏭️ Siguiente", "🔇 Mutear"],
        ["🖱️ Izquierda", "🖱️ Arriba", "🖱️ Derecha"],
        ["🖱️ Click", "🖱️ Abajo", "🖱️ Doble Click"],
        ["⌨️ Capturar Pantalla", "⌨️ Enter"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("🖥️ Conectado a Linux. Usa los botones o escribe texto para enviarlo al teclado.", reply_markup=reply_markup)

# Manejador de acciones (Botones y texto libre)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update):
        return

    text = update.message.text
    distancia_raton = 50  # Píxeles que se moverá el ratón por click

    # --- CONTROL DE MULTIMEDIA (Usa xdotool para simular teclas multimedia globales) ---
    if text == "⏯️ Play/Pausa":
        os.system("xdotool key XF86AudioPlay")
    elif text == "🎵 Vol+":
        os.system("xdotool key XF86AudioRaiseVolume")
    elif text == "🎵 Vol-":
        os.system("xdotool key XF86AudioLowerVolume")
    elif text == "⏮️ Anterior":
        os.system("xdotool key XF86AudioPrev")
    elif text == "⏭️ Siguiente":
        os.system("xdotool key XF86AudioNext")
    elif text == "🔇 Mutear":
        os.system("xdotool key XF86AudioMute")

    # --- CONTROL DEL RATÓN ---
    elif text == "🖱️ Arriba":
        pyautogui.moveRel(0, -distancia_raton)
    elif text == "🖱️ Abajo":
        pyautogui.moveRel(0, distancia_raton)
    elif text == "🖱️ Izquierda":
        pyautogui.moveRel(-distancia_raton, 0)
    elif text == "🖱️ Derecha":
        pyautogui.moveRel(distancia_raton, 0)
    elif text == "🖱️ Click":
        pyautogui.click()
    elif text == "🖱️ Doble Click":
        pyautogui.doubleClick()

    # --- CONTROL DE TECLADO Y ACCIONES ---
    elif text == "⌨️ Enter":
        pyautogui.press('enter')
    elif text == "⌨️ Capturar Pantalla":
        screenshot_path = "/tmp/screenshot.png"
        pyautogui.screenshot(screenshot_path)
        with open(screenshot_path, 'rb') as photo:
            await update.message.reply_photo(photo=photo, caption="📸 Captura actual de tu pantalla")
        os.remove(screenshot_path)
    
    # Si escribes cualquier otra cosa, el PC lo tecleará textualmente
    else:
        pyautogui.write(text)
        await update.message.reply_text(f"⌨️ Tecleado: '{text}'")

def main():
    # Crear la aplicación con la librería python-telegram-bot (v20+)
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot en marcha... Presiona Ctrl+C para detenerlo.")
    application.run_polling()

if __name__ == '__main__':
    main()
