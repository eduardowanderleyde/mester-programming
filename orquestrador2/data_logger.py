import csv
import json
import os
from datetime import datetime
from config import STORAGE_TYPE, CSV_FILE, JSON_FILE
import gzip
import shutil

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
MAX_FILES = 5

def rotate_file(file_path):
    if not os.path.exists(file_path):
        return
    
    if os.path.getsize(file_path) < MAX_FILE_SIZE:
        return
    
    # Criar backup comprimido
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{file_path}.{timestamp}.gz"
    
    with open(file_path, 'rb') as f_in:
        with gzip.open(backup_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    
    # Limpar arquivo original
    open(file_path, 'w').close()
    
    # Manter apenas os últimos MAX_FILES backups
    backup_files = sorted([f for f in os.listdir('.') if f.startswith(file_path) and f.endswith('.gz')])
    for old_file in backup_files[:-MAX_FILES]:
        os.remove(old_file)

def save_data(data):
    if STORAGE_TYPE == "csv":
        save_to_csv(data)
    elif STORAGE_TYPE == "json":
        save_to_json(data)

def save_to_csv(data):
    rotate_file(CSV_FILE)
    
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())
        if file.tell() == 0:  # Se o arquivo estiver vazio, escrever cabeçalho
            writer.writeheader()
        writer.writerow(data)

def save_to_json(data):
    rotate_file(JSON_FILE)
    
    with open(JSON_FILE, "a") as file:
        json.dump(data, file)
        file.write("\n")

if __name__ == "__main__":
    sample_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "wifi": [{"SSID": "wanderley", "BSSID": "00:11:22:33:44:55", "Signal Level (dBm)": -50}],
        "latency": {"latency_ms": 20.5, "packet_loss": False},
        "bandwidth": {"bandwidth_mbps": 50.2},
        "handover": {"handover": False}
    }
    save_data(sample_data)
