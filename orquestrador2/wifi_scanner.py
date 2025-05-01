import subprocess
import re
import time
from datetime import datetime
import json
import random

def scan_wifi():
    try:
        # Dados simulados para teste
        signal_level = random.randint(-80, -30)  # Valores típicos de RSSI
        noise_level = -100
        quality = signal_level - noise_level
        
        wifi_info = [{
            "SSID": "Rede-Teste-Mesh",
            "BSSID": "00:11:22:33:44:55",
            "Signal Level (dBm)": signal_level,
            "Quality": f"{quality}/70",
            "Channel": "36",
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }]
        
        return wifi_info
            
    except Exception as e:
        print(f"Erro inesperado: {str(e)}")
        return []

if __name__ == "__main__":
    while True:
        result = scan_wifi()
        if result:
            print(json.dumps(result, indent=2))
        time.sleep(1)
