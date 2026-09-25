#!/bin/bash

# Colores para la terminal
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # Sin color

echo -e "${BLUE}[*] Instalando dependencias del sistema...${NC}"
sudo apt update && sudo apt install -y xdotool

echo -e "${BLUE}[*] Instalando librerías de Python...${NC}"
pip install -r requirements.txt

echo -e "${BLUE}[*] Configurando el servicio de Systemd...${NC}"
# Obtener rutas dinámicamente para evitar fallos si cambia de usuario o carpeta
USER_ACTUAL=$(whoami)
DIR_ACTUAL=$(pwd)
PYTHON_PATH=$(which python)

sudo bash -c "cat << 'EOF' > /etc/systemd/system/tgbot.service
[Unit]
Description=Bot de Telegram para Controlar PC Linux
After=network.target graphical.target

[Service]
Type=simple
User=$USER_ACTUAL
WorkingDirectory=$DIR_ACTUAL
Environment=DISPLAY=:0
ExecStart=$PYTHON_PATH bot.py
Restart=on-failure
RestartSec=5

[Install]
WantedBy=graphical.target
EOF"

echo -e "${BLUE}[*] Activando e iniciando el servicio...${NC}"
sudo systemctl daemon-reload
sudo systemctl enable tgbot.service
sudo systemctl start tgbot.service

echo -e "${GREEN}[+] ¡Instalación completada con éxito!${NC}"
echo -e "${GREEN}[+] El bot ya está corriendo en segundo plano.${NC}"
echo -e "${BLUE}[*] Puedes comprobar el estado con: sudo systemctl status tgbot.service${NC}"
