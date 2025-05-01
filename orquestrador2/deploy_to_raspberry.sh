#!/bin/bash

# Configurar IP do Raspberry Pi
RASPBERRY_IP="192.168.68.107"  # IP do seu Raspberry Pi
RASPBERRY_USER="eduardowanderley"  # Usuário correto do Raspberry Pi
RASPBERRY_PASS="200982"  # Senha do Raspberry Pi
PROJECT_DIR="mesh-monitor"

echo "Iniciando deployment para o Raspberry Pi..."

# Criar diretório remoto
sshpass -p "$RASPBERRY_PASS" ssh $RASPBERRY_USER@$RASPBERRY_IP "rm -rf ~/$PROJECT_DIR && mkdir -p ~/$PROJECT_DIR/templates"

# Transferir todos os arquivos Python
echo "Transferindo arquivos Python..."
sshpass -p "$RASPBERRY_PASS" scp *.py $RASPBERRY_USER@$RASPBERRY_IP:~/$PROJECT_DIR/

# Transferir templates
echo "Transferindo templates..."
sshpass -p "$RASPBERRY_PASS" scp -r templates/* $RASPBERRY_USER@$RASPBERRY_IP:~/$PROJECT_DIR/templates/

# Transferir script de setup
echo "Transferindo script de setup..."
sshpass -p "$RASPBERRY_PASS" scp setup_raspberry.sh $RASPBERRY_USER@$RASPBERRY_IP:~/$PROJECT_DIR/

# Executar script de setup
echo "Executando setup no Raspberry Pi..."
sshpass -p "$RASPBERRY_PASS" ssh $RASPBERRY_USER@$RASPBERRY_IP "cd ~/$PROJECT_DIR && chmod +x setup_raspberry.sh && ./setup_raspberry.sh"

echo "Deployment concluído!"
echo "Iniciando o serviço..."
sshpass -p "$RASPBERRY_PASS" ssh $RASPBERRY_USER@$RASPBERRY_IP "cd ~/$PROJECT_DIR && python3 main.py &"
echo "Acesse http://$RASPBERRY_IP:8080 para ver o monitor" 