import subprocess
import re

def measure_latency():
    try:
        result = subprocess.run(["ping", "-c", "5", "8.8.8.8"], text=True, capture_output=True)
        match = re.search(r"(\d+)% packet loss", result.stdout)
        packet_loss = int(match.group(1)) if match else 0

        match = re.search(r"min/avg/max/mdev = ([\d\.]+)/([\d\.]+)/([\d\.]+)/([\d\.]+)", result.stdout)
        latency = float(match.group(2)) if match else None

        return {"latency_ms": latency, "packet_loss": packet_loss > 0}

    except:
        return {"error": "Erro ao executar ping"}

if __name__ == "__main__":
    print(measure_latency())
