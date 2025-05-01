import subprocess
import time
from datetime import datetime

def get_battery_level():
    try:
        # Comando para obter informações da bateria (ajuste conforme seu sistema)
        result = subprocess.check_output(["upower", "-i", "/org/freedesktop/UPower/devices/battery_BAT0"], text=True)
        
        # Extrair nível da bateria
        percentage = re.search(r'percentage:\s+(\d+)%', result)
        if percentage:
            return int(percentage.group(1))
        
        return None
    except Exception as e:
        print(f"Erro ao ler nível da bateria: {str(e)}")
        return None

def adjust_interval(battery_level):
    if battery_level is None:
        return 10  # Intervalo padrão
        
    if battery_level < 20:
        return 30  # Intervalo maior para economizar bateria
    elif battery_level < 50:
        return 20  # Intervalo médio
    else:
        return 10  # Intervalo normal

if __name__ == "__main__":
    while True:
        battery_level = get_battery_level()
        if battery_level is not None:
            print(f"Bateria: {battery_level}%")
            print(f"Intervalo ajustado para: {adjust_interval(battery_level)} segundos")
        time.sleep(5) 