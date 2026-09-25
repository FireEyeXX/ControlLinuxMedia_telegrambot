
import os
import subprocess
import logging
import webbrowser
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import pyautogui

# --- CONFIGURACIÓN DE SEGURIDAD ---
# NOTA: Se recomienda usar variables de entorno para proteger tu token.
TOKEN = "TOKEN_DE_TU_TELEGRAM_BOT"
ADMIN_ID = 1234567890  Reemplaza con tu ID numérico de Telegram 

# Configuración de PyAutoGUI
pyautogui.PAUSE = 0.05
pyautogui.FAILSAFE = True  # Mover el ratón a una esquina aborta acciones si algo falla

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Diccionario para guardar el estado o configuraciones temporales de cada usuario
USER_SETTINGS = {}

def is_admin(update: Update) -> bool:
    return update.effective_user.id == ADMIN_ID

# --- MENÚS DE NAVEGACIÓN ---
def get_main_menu():
    return ReplyKeyboardMarkup([
        ["🎵 Multimedia", "🖱️ Ratón", "⌨️ Teclado"],
        ["🌐 Navegador & YT", "💻 Sistema & CMD", "⚙️ Ajustes"]
    ], resize_keyboard=True)

def get_multimedia_menu():
    return ReplyKeyboardMarkup([
        ["🎵 Vol-", "🎵 Vol+", "🔇 Mutear"],
        ["⏮️ Anterior", "⏯️ Play/Pausa", "⏭️ Siguiente"],
        ["🔅 Brillo -", "🔆 Brillo +", "🔙 Volver al Menú"]
    ], resize_keyboard=True)

def get_mouse_menu():
    return ReplyKeyboardMarkup([
        ["🖱️ Izquierda", "🖱️ Arriba", "🖱️ Derecha"],
        ["🖱️ Click", "🖱️ Abajo", "🖱️ Doble Click"],
        ["🖱️ Click Der.", "🖱️ Scroll Arriba", "🖱️ Scroll Abajo"],
        ["🔙 Volver al Menú"]
    ], resize_keyboard=True)

def get_keyboard_menu():
    return ReplyKeyboardMarkup([
        ["⌨️ Capturar Pantalla", "⌨️ Enter", "⌨️ Borrar"],
        ["⌨️ Espacio", "⌨️ Alt+Tab", "⌨️ Esc"],
        ["🔙 Volver al Menú"]
    ], resize_keyboard=True)

def get_browser_menu():
    return ReplyKeyboardMarkup([
        ["📺 Abrir YouTube", "🔍 Buscar en YT", "🎧 YT Lo-Fi"],
        ["🌐 Abrir Google", "➕ Nueva Pestaña", "❌ Cerrar Pestaña"],
        ["🔙 Volver al Menú"]
    ], resize_keyboard=True)

def get_system_menu():
    return ReplyKeyboardMarkup([
        ["🖥️ Estado PC", "🐚 Ejecutar CMD", "🔒 Bloquear PC"],
        ["⚠️ Reiniciar PC", "🛑 Apagar PC"],
        ["🔙 Volver al Menú"]
    ], resize_keyboard=True)

def get_settings_menu():
    return ReplyKeyboardMarkup([
        ["⚡ Ratón Rápido (100px)", "🐢 Ratón Lento (20px)"],
        ["🔙 Volver al Menú"]
    ], resize_keyboard=True)


# --- COMANDOS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update):
        await update.message.reply_text("❌ No estás autorizado para controlar esta PC.")
        return
    
    # Inicializar distancia por defecto si no existe
    USER_SETTINGS[update.effective_user.id] = {"mouse_dist": 50, "waiting_cmd": False, "waiting_yt": False}
    
    await update.message.reply_text(
        "🖥️ **Panel de Control Avanzado Linux**\n\nSelecciona una categoría para desplegar las herramientas de control.",
        reply_markup=get_main_menu(),
        parse_mode="Markdown"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update):
        return

    uid = update.effective_user.id
    if uid not in USER_SETTINGS:
        USER_SETTINGS[uid] = {"mouse_dist": 50, "waiting_cmd": False, "waiting_yt": False}

    text = update.message.text
    settings = USER_SETTINGS[uid]

    # --- FLUJOS DE ENTRADA DE TEXTO ESPECIALES ---
    if settings["waiting_cmd"]:
        settings["waiting_cmd"] = False
        try:
            # Ejecuta comandos en la terminal de Linux de forma segura y devuelve la salida
            resultado = subprocess.run(text, shell=True, capture_output=True, text=True, timeout=10)
            salida = resultado.stdout if resultado.stdout else resultado.stderr
            if not salida:
                salida = "Comando ejecutado sin retorno de texto."
            await update.message.reply_text(f"🐚 **Salida de Terminal:**\n```\n{salida[:4000]}\n```", parse_mode="Markdown")
        except Exception as e:
            await update.message.reply_text(f"❌ Error al ejecutar el comando: {e}")
        return

    if settings["waiting_yt"]:
        settings["waiting_yt"] = False
        url = f"https://youtube.com{text.replace(' ', '+')}"
        webbrowser.open(url)
        await update.message.reply_text(f"🔍 Buscando '{text}' en YouTube en tu PC...")
        return

    # --- CAMBIOS DE MENÚ ---
    if text == "🔙 Volver al Menú":
        await update.message.reply_text("🏠 Menú Principal", reply_markup=get_main_menu())
    elif text == "🎵 Multimedia":
        await update.message.reply_text("🎵 Control de Medios y Pantalla", reply_markup=get_multimedia_menu())
    elif text == "🖱️ Ratón":
        await update.message.reply_text("🖱️ Control de Cursor y Scroll", reply_markup=get_mouse_menu())
    elif text == "⌨️ Teclado":
        await update.message.reply_text("⌨️ Atajos y Escritura Avanzada", reply_markup=get_keyboard_menu())
    elif text == "🌐 Navegador & YT":
        await update.message.reply_text("🌐 Integración con Navegador Web", reply_markup=get_browser_menu())
    elif text == "💻 Sistema & CMD":
        await update.message.reply_text("💻 Herramientas de Sistema y Consola", reply_markup=get_system_menu())
    elif text == "⚙️ Ajustes":
        await update.message.reply_text("⚙️ Configuración del Bot", reply_markup=get_settings_menu())

    # --- ACCIONES MULTIMEDIA ---
    elif text == "⏯️ Play/Pausa":
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
    elif text == "🔅 Brillo -":
        os.system("xdotool key XF86MonBrightnessDown")
    elif text == "🔆 Brillo +":
        os.system("xdotool key XF86MonBrightnessUp")

    # --- ACCIONES DEL RATÓN ---
    elif text == "🖱️ Arriba":
        pyautogui.moveRel(0, -settings["mouse_dist"])
    elif text == "🖱️ Abajo":
        pyautogui.moveRel(0, settings["mouse_dist"])
    elif text == "🖱️ Izquierda":
        pyautogui.moveRel(-settings["mouse_dist"], 0)
    elif text == "🖱️ Derecha":
        pyautogui.moveRel(settings["mouse_dist"], 0)
    elif text == "🖱️ Click":
        pyautogui.click()
    elif text == "🖱️ Doble Click":
        pyautogui.doubleClick()
    elif text == "🖱️ Click Der.":
        pyautogui.click(button='right')
    elif text == "🖱️ Scroll Arriba":
        pyautogui.scroll(10)
    elif text == "🖱️ Scroll Abajo":
        pyautogui.scroll(-10)

    # --- ACCIONES DEL TECLADO ---
    elif text == "⌨️ Enter":
        pyautogui.press('enter')
    elif text == "⌨️ Borrar":
        pyautogui.press('backspace')
    elif text == "⌨️ Espacio":
        pyautogui.press('space')
    elif text == "⌨️ Alt+Tab":
        pyautogui.hotkey('alt', 'tab')
    elif text == "⌨️ Esc":
        pyautogui.press('esc')
    elif text == "⌨️ Capturar Pantalla":
        screenshot_path = "/tmp/screenshot.png"
        pyautogui.screenshot(screenshot_path)
        if os.path.exists(screenshot_path):
            with open(screenshot_path, 'rb') as photo:
                await update.message.reply_photo(photo=photo, caption="📸 Pantalla de tu PC")
            os.remove(screenshot_path)

    # --- INTEGRACIÓN NAVEGADOR & YOUTUBE ---
    elif text == "📺 Abrir YouTube":
        webbrowser.open("https://youtube.com")
        await update.message.reply_text("📺 Abriendo YouTube en tu PC...")
    elif text == "🔍 Buscar en YT":
        settings["waiting_yt"] = True
        await update.message.reply_text("📝 Escribe lo que quieres buscar en YouTube:")
    elif text == "🎧 YT Lo-Fi":
        webbrowser.open("https://youtube.com/watch?v=jfKfPfyJRdk")  # Radio en vivo clásica Lofi
        await update.message.reply_text("🎧 Poniento música Lo-Fi en YouTube...")
    elif text == "🌐 Abrir Google":
        webbrowser.open("https://google.com")
        await update.message.reply_text("🌐 Abriendo Google...")
    elif text == "➕ Nueva Pestaña":
        pyautogui.hotkey('ctrl', 't')
    elif text == "❌ Cerrar Pestaña":
        pyautogui.hotkey('ctrl', 'w')

    # --- INTEGRACIONES DE SISTEMA ---
    elif text == "🖥️ Estado PC":
        try:
            # Obtener uso de CPU y memoria mediante comandos básicos de Linux
            cpu = subprocess.getoutput("top -bn1 | grep 'Cpu(s)' | awk '{print $2 + $4}'")
            ram = subprocess.getoutput("free -m | awk 'NR==2{printf \"%.2f%% (Usado: %sMB / Total: %sMB)\", $3*100/$2, $3, $2}'")
            uptime = subprocess.getoutput("uptime -p")
            info = f"📊 **Estado de tu PC Linux:**\n\n💻 **Uso de CPU:** {cpu}%\n🧠 **Uso de RAM:** {ram}\n⏱️ **Uptime:** {uptime}"
            await update.message.reply_text(info, parse_mode="Markdown")
        except Exception as e:
            await update.message.reply_text(f"No se pudo obtener el estado: {e}")
    elif text == "🐚 Ejecutar CMD":
        settings["waiting_cmd"] = True
        await update.message.reply_text("🐚 Envía el comando de terminal (Bash) que deseas ejecutar:")
    elif text == "🔒 Bloquear PC":
        await update.message.reply_text("🔒 Bloqueando pantalla...")
        os.system("xdg-screensaver lock || gnome-screensaver-command -l")
    elif text == "⚠️ Reiniciar PC":
        await update.message.reply_text("🔄 Reiniciando el equipo...")
        os.system("reboot")
    elif text == "🛑 Apagar PC":
        await update.message.reply_text("🛑 Apagando el equipo...")
        os.system("shutdown now")

    # --- AJUSTES ---
    elif text == "⚡ Ratón Rápido (100px)":
        settings["mouse_dist"] = 100
        await update.message.reply_text("⚡ Sensibilidad fijada en 100 píxeles.")
        
    elif text == "🐢 Ratón Lento (20px)":
        settings["mouse_dist"] = 20
        await update.message.reply_text("🐢 Sensibilidad fijada en 20 píxeles.")

    # --- ESCRITURA DIRECTA DE TEXTO ---
    else:
        # Si no coincide con un botón, teclea el texto enviado
        pyautogui.write(text)
        await update.message.reply_text(f"⌨️ Texto tecleado en PC: '{text}'")
def main():
    # Crear la aplicación con la librería python-telegram-bot
    application = Application.builder().token(TOKEN).build()

    # Añadir los manejadores de comandos y mensajes
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot Premium en marcha... Presiona Ctrl+C para detenerlo.")
    
    # Iniciar el bot en modo polling
    application.run_polling()

if __name__ == '__main__':
    main()
                                     
  
