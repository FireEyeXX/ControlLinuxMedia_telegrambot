 
# 🖥️ ControlLinuxMedia_telegrambot
Bot de telegram para controlar teclado, raton, volumen...

Un bot de Telegram escrito en Python que te permite emular el uso del **ratón, teclado y controlar la reproducción multimedia** de tu ordenador con Linux de forma remota y segura.

## ✨ Características
*   🎵 **Control Multimedia:** Subir/bajar volumen, reproducir, pausar y cambiar de pista.
*   🖱️ **Control del Ratón:** Movimiento direccional mediante botones, click simple y doble click.
*   ⌨️ **Control del Teclado:** Envió de texto directo y simulación de la tecla *Enter*.
*   📸 **Capturas de Pantalla:** Recibe una imagen en tiempo real de lo que ocurre en tu monitor.
*   🔒 **Seguridad Integrada:** El bot solo responde a los comandos del administrador configurado.

## 🛠️ Requisitos del Sistema (Linux)
El script requiere `xdotool` para interactuar con la interfaz gráfica. Instálalo ejecutando:

```bash
sudo apt update && sudo apt install -y xdotool
```
*Nota: Si utilizas entornos modernos basados en Wayland, asegúrate de iniciar sesión seleccionando la sesión **X11 / Xorg** en la pantalla de bloqueo para que la emulación del ratón funcione correctamente.*

## 🚀 Instalación y Uso

1.  **Clona este repositorio o descarga los archivos:**
    ```bash
    git clone <URL_DE_TU_REPOSITORIO>
    cd <NOMBRE_CARPETA>
    ```

2.  **Instala las dependencias necesarias:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configura tus credenciales:**
    Abre el archivo `bot.py` y edita las siguientes variables con tu Token de BotFather y tu ID de usuario de Telegram:
    ```python
    TOKEN = "TU_TELEGRAM_BOT_TOKEN"
    ADMIN_ID = 123456789  # Tu ID numérico
    ```

4.  **Inicia el bot:**
    ```bash
    python bot.py
    ```

5.  Abre el chat con tu bot en Telegram y presiona `/start`.

## 📄 Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.
