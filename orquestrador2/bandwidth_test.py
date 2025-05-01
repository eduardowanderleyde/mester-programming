import subprocess
import json
import time
import socket

def check_iperf_server(host, port=5201):
    """Verifica se o servidor iperf3 está acessível"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

def measure_bandwidth():
    """Mede a largura de banda usando iperf3"""
    server_ip = "192.168.68.100"  # IP do servidor iperf3
    
    # Verifica se o servidor está acessível
    if not check_iperf_server(server_ip):
        return {
            "error": "Servidor iperf3 não está acessível",
            "bandwidth_mbps": 0,
            "details": "Verifique se o servidor está rodando e acessível"
        }
    
    try:
        # Executa o teste com parâmetros otimizados
        result = subprocess.run(
            [
                "iperf3",
                "-c", server_ip,      # Endereço do servidor
                "-f", "m",            # Formato em Mbits/sec
                "-t", "2",            # Duração do teste (2 segundos)
                "-i", "0.5",          # Intervalo de relatório
                "-J"                  # Saída em JSON
            ],
            text=True,
            capture_output=True,
            timeout=5                 # Timeout total de 5 segundos
        )

        if result.returncode != 0:
            return {
                "error": f"iperf3 falhou: {result.stderr}",
                "bandwidth_mbps": 0,
                "details": result.stdout
            }

        # Tenta parsear o resultado JSON
        try:
            data = json.loads(result.stdout)
            end_info = data.get('end', {})
            sum_info = end_info.get('sum_received', {})
            
            bandwidth = sum_info.get('bits_per_second', 0) / 1_000_000  # Convertendo para Mbps
            
            return {
                "bandwidth_mbps": round(bandwidth, 2),
                "retransmits": sum_info.get('retransmits', 0),
                "jitter_ms": round(sum_info.get('jitter_ms', 0), 2),
                "error": None
            }

        except json.JSONDecodeError:
            return {
                "error": "Erro ao processar resultado do iperf3",
                "bandwidth_mbps": 0,
                "details": result.stdout
            }

    except subprocess.TimeoutExpired:
        return {
            "error": "iperf3 timeout",
            "bandwidth_mbps": 0,
            "details": "O teste demorou muito para completar"
        }
    except Exception as e:
        return {
            "error": f"Erro inesperado: {str(e)}",
            "bandwidth_mbps": 0,
            "details": "Erro durante a execução do teste"
        }

if __name__ == "__main__":
    # Teste contínuo para debug
    while True:
        print("\nTestando bandwidth...")
        result = measure_bandwidth()
        print(json.dumps(result, indent=2))
        if result.get("error"):
            print(f"\nErro: {result['error']}")
            if result.get("details"):
                print(f"Detalhes: {result['details']}")
        time.sleep(5)
