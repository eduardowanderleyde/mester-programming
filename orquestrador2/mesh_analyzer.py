import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np
from collections import defaultdict

class MeshAnalyzer:
    def __init__(self):
        self.history = defaultdict(list)
        self.handover_events = []
        self.signal_threshold = -70  # dBm
        
    def add_measurement(self, wifi_data):
        """Adiciona nova medição ao histórico"""
        timestamp = datetime.now()
        if isinstance(wifi_data, list):
            for ap in wifi_data:
                bssid = ap.get('BSSID')
                signal = ap.get('Signal Level (dBm)')
                if bssid and signal:
                    self.history[bssid].append({
                        'timestamp': timestamp,
                        'signal': signal
                    })
                    
                    # Verifica handover
                    self._check_handover(bssid, signal)
    
    def _check_handover(self, current_bssid, current_signal):
        """Detecta handovers entre pontos mesh"""
        if not self.handover_events:
            self.handover_events.append({
                'timestamp': datetime.now(),
                'from_bssid': None,
                'to_bssid': current_bssid,
                'signal': current_signal
            })
            return
            
        last_handover = self.handover_events[-1]
        if last_handover['to_bssid'] != current_bssid:
            self.handover_events.append({
                'timestamp': datetime.now(),
                'from_bssid': last_handover['to_bssid'],
                'to_bssid': current_bssid,
                'signal': current_signal
            })
    
    def generate_signal_graph(self, output_file='signal_history.png'):
        """Gera gráfico da força do sinal ao longo do tempo"""
        plt.figure(figsize=(12, 6))
        
        for bssid, measurements in self.history.items():
            times = [m['timestamp'] for m in measurements]
            signals = [m['signal'] for m in measurements]
            plt.plot(times, signals, label=f'AP: {bssid[-8:]}')
        
        plt.axhline(y=self.signal_threshold, color='r', linestyle='--', label='Limiar de Sinal')
        plt.title('Histórico de Força do Sinal por Ponto de Acesso')
        plt.xlabel('Tempo')
        plt.ylabel('Força do Sinal (dBm)')
        plt.legend()
        plt.grid(True)
        plt.savefig(output_file)
        plt.close()
    
    def analyze_handovers(self):
        """Analisa padrões de handover"""
        if not self.handover_events:
            return "Nenhum handover detectado ainda"
            
        analysis = {
            'total_handovers': len(self.handover_events) - 1,
            'avg_time_between_handovers': None,
            'most_common_transition': None
        }
        
        if len(self.handover_events) > 2:
            times_between = []
            for i in range(1, len(self.handover_events)):
                delta = self.handover_events[i]['timestamp'] - self.handover_events[i-1]['timestamp']
                times_between.append(delta.total_seconds())
            
            analysis['avg_time_between_handovers'] = sum(times_between) / len(times_between)
            
        return analysis
    
    def get_signal_quality_summary(self):
        """Resumo da qualidade do sinal"""
        summary = {}
        for bssid, measurements in self.history.items():
            signals = [m['signal'] for m in measurements]
            summary[bssid] = {
                'min_signal': min(signals),
                'max_signal': max(signals),
                'avg_signal': sum(signals) / len(signals),
                'measurements_count': len(signals)
            }
        return summary

    def get_handover_history(self):
        """Retorna o histórico de handovers"""
        return self.handover_events

    def get_signal_history(self):
        """Retorna o histórico de sinais"""
        signal_history = []
        for bssid, measurements in self.history.items():
            for m in measurements:
                signal_history.append({
                    'timestamp': m['timestamp'],
                    'signal': m['signal'],
                    'bssid': bssid
                })
        return sorted(signal_history, key=lambda x: x['timestamp'])

    def get_current_signal(self):
        """Retorna o sinal atual do último AP conectado"""
        if not self.handover_events:
            return None
        last_bssid = self.handover_events[-1]['to_bssid']
        if last_bssid in self.history and self.history[last_bssid]:
            return self.history[last_bssid][-1]['signal']
        return None

    def get_current_latency(self):
        """Retorna a latência atual (placeholder)"""
        return None

if __name__ == "__main__":
    analyzer = MeshAnalyzer()
    # Exemplo de uso
    test_data = [
        {'BSSID': '00:11:22:33:44:55', 'Signal Level (dBm)': -65},
        {'BSSID': '66:77:88:99:AA:BB', 'Signal Level (dBm)': -55}
    ]
    analyzer.add_measurement(test_data)
    print(analyzer.get_signal_quality_summary()) 