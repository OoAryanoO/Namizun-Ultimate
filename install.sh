#!/bin/bash

GITHUB_RAW_URL="https://raw.githubusercontent.com/OoAryanoO/Namizun-Ultimate/main/namizun2.py"
INSTALL_DIR="/usr/local/bin"
SCRIPT_NAME="namizun"
SERVICE_NAME="namizun.service"

GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

if [ "$EUID" -ne 0 ]; then
  echo -e "${RED}Please run as root (sudo).${NC}"
  exit
fi

clear
echo -e "${BLUE}=========================================${NC}"
echo -e "${BLUE}    NAMIZUN 2 ULTIMATE - INSTALLER       ${NC}"
echo -e "${BLUE}=========================================${NC}"
echo ""

echo -e "${GREEN}[+] Updating system and installing dependencies...${NC}"
if [ -f /etc/debian_version ]; then
    apt-get update -q
    apt-get install -y python3 python3-pip wget -q
elif [ -f /etc/redhat-release ]; then
    yum update -q
    yum install -y python3 python3-pip wget -q
fi

echo -e "${GREEN}[+] Installing Python libraries (psutil)...${NC}"
pip3 install psutil > /dev/null 2>&1

echo -e "${GREEN}[+] Downloading Namizun core script...${NC}"
rm -f "$INSTALL_DIR/$SCRIPT_NAME"
wget -q -O "$INSTALL_DIR/$SCRIPT_NAME" "$GITHUB_RAW_URL"

if [ $? -ne 0 ]; then
    echo -e "${RED}[!] Failed to download script. Check your internet or GitHub URL.${NC}"
    exit 1
fi

sed -i 's/\r$//' "$INSTALL_DIR/$SCRIPT_NAME"

chmod +x "$INSTALL_DIR/$SCRIPT_NAME"

echo -e "${GREEN}[+] Creating systemd service...${NC}"
cat > /etc/systemd/system/$SERVICE_NAME <<EOF
[Unit]
Description=Namizun 2 Service
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 $INSTALL_DIR/$SCRIPT_NAME run
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable $SERVICE_NAME > /dev/null 2>&1
systemctl restart $SERVICE_NAME

echo -e "${BLUE}=========================================${NC}"
echo -e "${GREEN}✓ INSTALLATION COMPLETE!${NC}"
echo -e "${BLUE}=========================================${NC}"
echo -e "Type \033[1;33mnamizun\033[0m to open the menu."
echo -e "The background service is already running."
echo ""



