<div align="center">

# 🖥️ ControlLinuxMedia Telegram Bot

**Controla tu escritorio Linux de forma remota desde Telegram.**

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Telegram Bot API](https://img.shields.io/badge/Telegram-Bot%20API-26A5E4?logo=telegram&logoColor=white)](https://core.telegram.org/bots/api)
[![Linux](https://img.shields.io/badge/Linux-X11-FCC624?logo=linux&logoColor=black)](https://www.linux.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Bot de Telegram escrito en Python para manejar multimedia, ratón, teclado, navegador y algunas funciones del sistema en un equipo Linux.

</div>

> ⚠️ **Proyecto de uso personal.** Este bot puede ejecutar comandos en el equipo y apagarlo o reiniciarlo. Instálalo únicamente en ordenadores que controles, protege el token y no expongas el bot a usuarios no autorizados.

## 📌 Índice

- [Características](#-características)
- [Cómo funciona](#-cómo-funciona)
- [Requisitos](#-requisitos)
- [Instalación rápida](#-instalación-rápida)
- [Configuración](#-configuración)
- [Uso](#-uso)
- [Ejecución como servicio](#-ejecución-como-servicio)
- [Seguridad](#-seguridad)
- [Solución de problemas](#-solución-de-problemas)
- [Estructura del proyecto](#-estructura-del-proyecto)
- [Limitaciones conocidas](#-limitaciones-conocidas)
- [Contribuir](#-contribuir)
- [Licencia](#-licencia)

## ✨ Características

### 🎵 Multimedia y pantalla

- Subir y bajar el volumen.
- Silenciar el audio.
- Reproducir, pausar y cambiar de pista.
- Aumentar y reducir el brillo mediante teclas multimedia.

### 🖱️ Ratón

- Mover el cursor arriba, abajo, izquierda y derecha.
- Click izquierdo, click derecho y doble click.
- Scroll vertical.
- Dos sensibilidades configurables: 20 px y 100 px.

### ⌨️ Teclado y pantalla

- Escribir texto recibido desde Telegram en la ventana activa.
- Teclas Enter, Espacio, Escape y Backspace.
- Atajo Alt+Tab.
- Capturas de pantalla enviadas directamente al chat.

### 🌐 Navegador

- Abrir YouTube y Google.
- Buscar vídeos en YouTube.
- Abrir una emisora Lo-Fi.
- Crear y cerrar pestañas con atajos de teclado.

### 💻 Sistema

- Consultar CPU, memoria RAM y uptime.
- Bloquear la pantalla.
- Ejecutar comandos Bash y devolver su salida.
- Reiniciar o apagar el equipo.

## 🔄 Cómo funciona

1. `bot.py` inicia un cliente de Telegram usando `python-telegram-bot` en modo polling.
2. El bot acepta `/start` y mensajes de texto únicamente del `ADMIN_ID` configurado.
3. Los botones del teclado de Telegram se traducen en acciones locales mediante `PyAutoGUI`, `xdotool`, `subprocess` o `webbrowser`.
4. `install.sh` instala `xdotool` y las dependencias Python, y opcionalmente registra el bot como servicio de `systemd`.

## ✅ Requisitos

- Linux con una sesión gráfica **X11/Xorg** activa.
- Python 3.9 o superior recomendado.
- `pip` y `git`.
- `xdotool`.
- Un bot creado mediante [@BotFather](https://t.me/BotFather).
- El ID numérico de tu cuenta de Telegram.

> **Wayland:** el proyecto utiliza `xdotool` y automatización de escritorio orientada a X11. En Wayland algunas funciones pueden no funcionar o estar restringidas. Selecciona una sesión Xorg/X11 si necesitas control completo.

## 🚀 Instalación rápida

### 1. Clonar el repositorio

```bash
git clone https://github.com/FireEyeXX/ControlLinuxMedia_telegrambot.git
cd ControlLinuxMedia_telegrambot
```

### 2. Crear un entorno virtual

Se recomienda aislar las dependencias del proyecto:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

### 3. Instalar dependencias del sistema y Python

```bash
sudo apt update
sudo apt install -y xdotool python3-tk python3-dev scrot
python -m pip install -r requirements.txt
```

`python3-tk` y `scrot` pueden ser necesarios para que las capturas de pantalla funcionen correctamente según la distribución y el entorno gráfico.

### 4. Configurar y ejecutar

Edita `bot.py` y sustituye los valores de ejemplo:

```python
TOKEN = "TU_TOKEN_DE_TELEGRAM"
ADMIN_ID = 123456789
```

Después inicia el bot:

```bash
python bot.py
```

Abre el chat con tu bot en Telegram y envía `/start`.

## ⚙️ Configuración

### Crear el token

1. Abre Telegram y busca [@BotFather](https://t.me/BotFather).
2. Ejecuta `/newbot`.
3. Sigue las instrucciones y copia el token generado.

### Obtener tu `ADMIN_ID`

Puedes usar un bot como [@userinfobot](https://t.me/userinfobot) para consultar tu ID numérico. Solo ese usuario podrá controlar el equipo, siempre que el valor coincida con `ADMIN_ID`.

> **Recomendación:** no publiques el token ni lo guardes en commits. La versión actual usa placeholders en `bot.py`; para producción es preferible modificar el código para leer `TOKEN` y `ADMIN_ID` desde variables de entorno o un archivo de credenciales protegido.

## 🛠️ Instalación automática con `systemd`

El script incluido instala `xdotool`, instala `requirements.txt` y crea el servicio `tgbot.service` para iniciar el bot automáticamente con el entorno gráfico:

```bash
chmod +x install.sh
./install.sh
```

Ejecuta el instalador desde la raíz del repositorio. El script utiliza la ruta actual y el intérprete Python encontrado mediante `which python`.

### Comandos del servicio

```bash
# Consultar estado
sudo systemctl status tgbot.service

# Ver logs en tiempo real
journalctl -u tgbot.service -f

# Reiniciar después de cambiar la configuración
sudo systemctl restart tgbot.service

# Detener
sudo systemctl stop tgbot.service

# Desactivar el inicio automático
sudo systemctl disable tgbot.service
```

> Si utilizas un entorno virtual, revisa `ExecStart` en `/etc/systemd/system/tgbot.service` para que apunte a `.venv/bin/python` en lugar del Python global.

## 🔒 Seguridad

Este bot controla un equipo real, por lo que debes tratarlo como una herramienta administrativa:

- Mantén el token privado. Si se filtra, revócalo inmediatamente desde BotFather.
- Configura un `ADMIN_ID` único y verifica que sea el correcto.
- No compartas el bot ni permitas que usuarios desconocidos interactúen con él.
- No ejecutes el bot en un equipo crítico sin probarlo primero.
- Revisa cuidadosamente cualquier comando enviado mediante **Ejecutar CMD**.
- Ten en cuenta que esa función usa `subprocess.run(..., shell=True)` y permite ejecutar comandos con los permisos del usuario del servicio.
- No expongas credenciales, archivos privados ni salidas de terminal en chats o capturas.
- Considera reemplazar las credenciales en el código por variables de entorno y permisos restrictivos.

## 🧩 Solución de problemas

### El bot no responde

Comprueba que el proceso está activo y revisa los logs:

```bash
ps aux | grep bot.py
journalctl -u tgbot.service -n 100 --no-pager
```

Verifica también que `TOKEN` y `ADMIN_ID` sean correctos y que el bot haya recibido `/start`.

### `xdotool` no controla el escritorio

Confirma que la sesión gráfica es X11/Xorg:

```bash
echo "$XDG_SESSION_TYPE"
which xdotool
```

Si el resultado de la primera orden es `wayland`, inicia una sesión Xorg/X11.

### PyAutoGUI no puede abrir la pantalla

Asegúrate de que `DISPLAY` apunta a la sesión gráfica correcta y de que el usuario del servicio tiene acceso a ella:

```bash
echo "$DISPLAY"
echo "$XAUTHORITY"
```

En instalaciones con `systemd`, puede ser necesario añadir `DISPLAY` y `XAUTHORITY` adecuados en el archivo del servicio.

### Las capturas de pantalla fallan

Instala los paquetes auxiliares de tu distribución. En Debian/Ubuntu:

```bash
sudo apt install -y python3-tk scrot
```

## 📁 Estructura del proyecto

```text
ControlLinuxMedia_telegrambot/
├── bot.py             # Bot de Telegram, menús y acciones locales
├── install.sh         # Instalación y configuración del servicio systemd
├── requirements.txt   # Dependencias Python
├── LICENSE            # Licencia MIT
└── README.md          # Documentación del proyecto
```

## ⚠️ Limitaciones conocidas

- El control de escritorio depende de una sesión gráfica local y está diseñado principalmente para X11.
- El servicio generado por `install.sh` asume una instalación basada en Debian/Ubuntu (`apt`) y una pantalla disponible en `:0`.
- El estado temporal de usuario se guarda en memoria y se pierde al reiniciar el proceso.
- No hay una suite de tests automatizados incluida actualmente.
- La ejecución de comandos de terminal es deliberadamente potente y debe considerarse una operación privilegiada, aunque el servicio se ejecute con el usuario configurado.

## 🤝 Contribuir

1. Crea un fork del repositorio.
2. Crea una rama descriptiva:

   ```bash
   git checkout -b mejora/documentacion
   ```

3. Realiza cambios pequeños y enfocados.
4. Prueba el bot en una sesión X11 antes de abrir un Pull Request.
5. Describe claramente los cambios y cualquier requisito adicional.

## 📄 Licencia

Este proyecto se distribuye bajo la [Licencia MIT](LICENSE).

---

<div align="center">

Hecho para administrar un escritorio Linux desde Telegram 🐧

</div>
