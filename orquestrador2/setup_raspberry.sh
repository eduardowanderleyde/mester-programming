#!/bin/bash

echo "Configurando monitoramento Wi-Fi Mesh..."

# Atualizar sistema
echo "Atualizando sistema..."
sudo apt-get update
sudo apt-get upgrade -y

# Instalar dependências do sistema
echo "Instalando dependências do sistema..."
sudo apt-get install -y python3-pip wireless-tools net-tools iperf3 python3-venv

# Criar e ativar ambiente virtual
echo "Configurando ambiente virtual Python..."
python3 -m venv ~/mesh-monitor/venv
source ~/mesh-monitor/venv/bin/activate

# Instalar dependências Python
echo "Instalando dependências Python..."
pip install flask flask-socketio psutil speedtest-cli requests

# Configurar permissões para iwlist sem senha
echo "Configurando permissões sudo..."
echo "$USER ALL=(ALL) NOPASSWD: /sbin/iwlist" | sudo tee /etc/sudoers.d/mesh-monitor

# Criar serviço systemd para iniciar automaticamente
echo "Configurando serviço automático..."
cat << EOF | sudo tee /etc/systemd/system/mesh-monitor.service
[Unit]
Description=Mesh Network Monitor
After=network.target

[Service]
ExecStart=$HOME/mesh-monitor/venv/bin/python $HOME/mesh-monitor/main.py
WorkingDirectory=$HOME/mesh-monitor
User=$USER
Group=$USER
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# Habilitar e iniciar o serviço
sudo systemctl daemon-reload
sudo systemctl enable mesh-monitor
sudo systemctl start mesh-monitor

echo "Instalação concluída!"
echo "O monitor está rodando em http://$(hostname -I | cut -d' ' -f1):8080"
echo "Para ver os logs: sudo journalctl -u mesh-monitor -f" 