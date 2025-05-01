import subprocess
import re
import time
from datetime import datetime

def scan_wifi():
    try:
        # Usando sudo para garantir acesso
        result = subprocess.check_output(["sudo", "iwlist", "wlan0", "scan"], text=True)
        
        # Extrair informações detalhadas
        ssid = re.findall(r'ESSID:"(.*?)"', result)
        bssid = re.findall(r'Address: (.*?)\n', result)
        signal = re.findall(r'Signal level=(-\d+)', result)
        frequency = re.findall(r'Frequency:(\d+\.\d+)', result)
        channel = re.findall(r'Channel:(\d+)', result)
        quality = re.findall(r'Quality=(\d+)/70', result)
        
        wifi_info = []
        for i in range(len(ssid)):
            # Removido o filtro para "wanderley"
            wifi_info.append({
                "SSID": ssid[i],
                "BSSID": bssid[i],
                "Signal Level (dBm)": int(signal[i]) if i < len(signal) else None,
                "Quality": f"{quality[i]}/70" if i < len(quality) else None,
                "Frequency (GHz)": float(frequency[i]) if i < len(frequency) else None,
                "Channel": int(channel[i]) if i < len(channel) else None,
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        
        if not wifi_info:
            print("Aviso: Nenhuma rede encontrada")
            return []
            
        return wifi_info

    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar iwlist: {str(e)}")
        return []
    except Exception as e:
        print(f"Erro inesperado: {str(e)}")
        return []

if __name__ == "__main__":
    while True:
        result = scan_wifi()
        if result:
            for network in result:
                print(f"\nRede: {network['SSID']}")
                print(f"BSSID: {network['BSSID']}")
                print(f"Sinal: {network['Signal Level (dBm)']} dBm")
                print(f"Qualidade: {network['Quality']}")
                print(f"Canal: {network['Channel']}")
        time.sleep(1) 