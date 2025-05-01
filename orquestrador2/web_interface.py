from flask import Flask, render_template
from flask_socketio import SocketIO
import json
from datetime import datetime
import threading
import time
import logging
import os

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Dados em tempo real
realtime_data = {
    'wifi': None,
    'latency': None,
    'bandwidth': None,
    'handover': None,
    'diagnostics': None,
    'battery': None
}

@app.route('/')
def index():
    logger.info("Acessando página principal")
    return render_template('index.html')

@app.route('/test')
def test():
    return "Servidor está funcionando!"

def update_realtime_data(data):
    """Atualiza os dados em tempo real e envia para os clientes"""
    global realtime_data
    realtime_data = data
    socketio.emit('update_data', data)

def get_web_interface():
    """Retorna a aplicação Flask e o SocketIO"""
    return app, socketio

if __name__ == "__main__":
    logger.info("Iniciando web_interface.py diretamente")
    socketio.run(app, host='0.0.0.0', port=8080) 