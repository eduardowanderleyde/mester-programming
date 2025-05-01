import curses
import time
from datetime import datetime
from wifi_scanner import scan_wifi
from battery_monitor import get_battery_level

def init_colors():
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Bom sinal
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Sinal médio
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)    # Sinal fraco
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)   # Informações gerais

def get_signal_color(signal_level):
    if signal_level > -60:
        return 1  # Verde
    elif signal_level > -70:
        return 2  # Amarelo
    else:
        return 3  # Vermelho

def display_info(stdscr):
    stdscr.clear()
    curses.curs_set(0)  # Esconde o cursor
    
    while True:
        stdscr.clear()
        
        # Obter informações
        wifi_data = scan_wifi()
        battery_level = get_battery_level()
        
        # Título
        stdscr.addstr(0, 0, "Monitor de Rede Mesh", curses.A_BOLD)
        stdscr.addstr(1, 0, "=" * 50)
        
        # Informações da bateria
        if battery_level is not None:
            stdscr.addstr(3, 0, f"Bateria: {battery_level}%", curses.color_pair(4))
        
        # Informações da rede
        if isinstance(wifi_data, list) and wifi_data:
            for i, network in enumerate(wifi_data):
                y = 5 + i * 3
                stdscr.addstr(y, 0, f"Rede: {network['SSID']}")
                stdscr.addstr(y + 1, 0, f"BSSID: {network['BSSID']}")
                
                signal_color = get_signal_color(network['Signal Level (dBm)'])
                stdscr.addstr(y + 2, 0, 
                    f"Sinal: {network['Signal Level (dBm)']} dBm",
                    curses.color_pair(signal_color))
        else:
            stdscr.addstr(5, 0, "Nenhuma rede encontrada", curses.color_pair(3))
        
        # Data e hora
        stdscr.addstr(curses.LINES - 2, 0, 
            f"Última atualização: {datetime.now().strftime('%H:%M:%S')}",
            curses.color_pair(4))
        
        stdscr.refresh()
        time.sleep(1)

def main():
    try:
        curses.wrapper(display_info)
    except KeyboardInterrupt:
        print("\nMonitor encerrado.")

if __name__ == "__main__":
    main() 