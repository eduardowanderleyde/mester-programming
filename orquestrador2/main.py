import time
import signal
import sys
import threading
from wifi_scanner_raspberry import scan_wifi
from latency_test import measure_latency
from bandwidth_test import measure_bandwidth
from handover_test import detect_handover
from data_logger import save_data
from battery_monitor import get_battery_level, adjust_interval
from display import main as display_main
from mesh_analyzer import MeshAnalyzer
from mesh_diagnostics import MeshDiagnostics
from web_interface import get_web_interface, update_realtime_data
import subprocess

# Inicializar analisador e diagnóstico
analyzer = MeshAnalyzer()
diagnostics = MeshDiagnostics()

# Obter a aplicação Flask e o SocketIO
app, socketio = get_web_interface()

# Função para garantir que processos do iperf3 sejam finalizados ao encerrar o script
def cleanup(signum, frame):
    print("\n🛑 Interrompendo... Finalizando processos.")
    # Gerar gráfico final
    analyzer.generate_signal_graph('signal_history_final.png')
    print("\n📊 Relatório Final:")
    print(analyzer.analyze_handovers())
    print("\n📡 Resumo da Qualidade do Sinal:")
    print(analyzer.get_signal_quality_summary())
    
    # Adicionar diagnóstico final
    print("\n🔍 Diagnóstico da Rede:")
    diagnostic_data = {
        'signal': analyzer.get_current_signal(),
        'latency': analyzer.get_current_latency(),
        'handover_history': analyzer.get_handover_history(),
        'signal_history': analyzer.get_signal_history()
    }
    problems = diagnostics.analyze_network_health(diagnostic_data)
    recommendations = diagnostics.get_recommendations(problems)
    
    print("\nProblemas Detectados:")
    for p in problems:
        print(f"\n{p['type']}: {p['description']}")
        print(f"Recomendação: {p['recommendation']}")
        
    print("\nRecomendações Gerais:")
    for r in recommendations:
        print(f"\nPrioridade {r['priority']}: {r['action']}")
        for step in r['steps']:
            print(f"- {step}")
    
    subprocess.run(["pkill", "-9", "iperf3"], text=True, capture_output=True)
    sys.exit(0)

# Capturar SIGINT (CTRL + C) e chamar a função de limpeza
signal.signal(signal.SIGINT, cleanup)

def collect_data():
    while True:
        print("📡 Iniciando testes da rede Wi-Fi Mesh...")

        wifi_data = scan_wifi()
        latency = measure_latency()
        
        try:
            bandwidth = measure_bandwidth()
        except Exception as e:
            bandwidth = {"error": f"Erro no iperf3: {str(e)}"}
        
        handover = detect_handover()

        # Adicionar dados ao analisador
        analyzer.add_measurement(wifi_data)

        # Estrutura dos dados coletados
        data = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "wifi": wifi_data,
            "latency": latency,
            "bandwidth": bandwidth,
            "handover": handover
        }

        print("Dados coletados:", data)  # Debug

        # Realizar diagnóstico
        diagnostic_data = {
            'signal': wifi_data[0]['Signal Level (dBm)'] if wifi_data else None,
            'latency': latency['latency_ms'],
            'signal_history': analyzer.get_signal_history()
        }

        print("Dados de diagnóstico:", diagnostic_data)  # Debug
        problems = diagnostics.analyze_network_health(diagnostic_data)
        
        # Adicionar diagnóstico aos dados
        data['diagnostics'] = {
            'problems': problems,
            'recommendations': diagnostics.get_recommendations(problems)
        }

        # Adicionar nível da bateria
        data['battery'] = {
            'level': get_battery_level()
        }

        # Salvar os dados
        save_data(data)

        # Atualizar interface web
        update_realtime_data(data)

        # Gerar gráfico a cada 10 medições
        if analyzer.history and sum(len(m) for m in analyzer.history.values()) % 10 == 0:
            analyzer.generate_signal_graph()

        print("✅ Dados coletados e salvos.")
        
        # Ajustar intervalo baseado na bateria
        battery_level = get_battery_level()
        interval = adjust_interval(battery_level)
        time.sleep(interval)

def main():
    # Iniciar thread para coleta de dados
    data_thread = threading.Thread(target=collect_data)
    data_thread.daemon = True
    data_thread.start()
    
    # Iniciar interface web na porta 8080
    socketio.run(app, host='0.0.0.0', port=8080)

if __name__ == "__main__":
    main()
