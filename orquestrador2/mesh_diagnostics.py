import numpy as np
from datetime import datetime, timedelta
from collections import defaultdict

class MeshDiagnostics:
    def __init__(self):
        self.thresholds = {
            'signal_weak': -70,          # dBm
            'signal_critical': -80,       # dBm
            'latency_high': 100,         # ms
            'latency_critical': 150,      # ms
            'handover_frequency': 5,      # eventos por minuto
            'packet_loss_threshold': 0.05 # 5% de perda
        }
        
        self.history = defaultdict(list)
        self.problems = []
        
    def analyze_signal_problems(self, signal_data):
        """Analisa problemas relacionados ao sinal"""
        problems = []
        
        # Verifica força do sinal
        if signal_data < self.thresholds['signal_critical']:
            problems.append({
                'type': 'CRITICAL',
                'category': 'SIGNAL',
                'description': f'Sinal muito fraco: {signal_data} dBm',
                'recommendation': 'Considere se aproximar do ponto de acesso ou verificar obstáculos'
            })
        elif signal_data < self.thresholds['signal_weak']:
            problems.append({
                'type': 'WARNING',
                'category': 'SIGNAL',
                'description': f'Sinal fraco: {signal_data} dBm',
                'recommendation': 'Performance pode ser afetada nesta localização'
            })
            
        return problems

    def analyze_latency_problems(self, latency_data):
        """Analisa problemas de latência"""
        problems = []
        
        if latency_data > self.thresholds['latency_critical']:
            problems.append({
                'type': 'CRITICAL',
                'category': 'LATENCY',
                'description': f'Latência muito alta: {latency_data}ms',
                'recommendation': 'Verifique interferências ou sobrecarga na rede'
            })
        elif latency_data > self.thresholds['latency_high']:
            problems.append({
                'type': 'WARNING',
                'category': 'LATENCY',
                'description': f'Latência elevada: {latency_data}ms',
                'recommendation': 'Performance pode ser afetada para aplicações em tempo real'
            })
            
        return problems

    def analyze_handover_problems(self, handover_history, timeframe_minutes=5):
        """Analisa problemas relacionados a handovers"""
        problems = []
        
        # Conta handovers no período
        recent_handovers = [h for h in handover_history 
                          if h['timestamp'] > datetime.now() - timedelta(minutes=timeframe_minutes)]
        
        handover_rate = len(recent_handovers) / timeframe_minutes
        
        if handover_rate > self.thresholds['handover_frequency']:
            problems.append({
                'type': 'WARNING',
                'category': 'HANDOVER',
                'description': f'Handovers frequentes: {handover_rate:.1f}/minuto',
                'recommendation': 'Você está em uma área de transição entre pontos mesh. Considere se mover para uma área com sinal mais estável'
            })
            
        # Analisa padrões de ping-pong
        if len(recent_handovers) >= 2:
            bssids = [h['to_bssid'] for h in recent_handovers]
            for i in range(len(bssids)-1):
                if bssids[i] == bssids[i+2]:  # Padrão A -> B -> A
                    problems.append({
                        'type': 'WARNING',
                        'category': 'HANDOVER',
                        'description': 'Detectado padrão de handover ping-pong',
                        'recommendation': 'Considere ajustar a posição para evitar transições frequentes'
                    })
                    break
                    
        return problems

    def analyze_mesh_coverage(self, signal_history):
        """Analisa problemas de cobertura da rede mesh"""
        problems = []
        
        # Analisa variação do sinal
        if len(signal_history) > 10:
            signals = [s['signal'] for s in signal_history[-10:]]
            signal_std = np.std(signals)
            
            if signal_std > 15:  # Variação significativa
                problems.append({
                    'type': 'WARNING',
                    'category': 'COVERAGE',
                    'description': f'Sinal instável (variação: {signal_std:.1f} dBm)',
                    'recommendation': 'Área com cobertura irregular. Considere reposicionar os pontos mesh'
                })
                
        return problems

    def analyze_network_health(self, data):
        """Análise completa da saúde da rede"""
        all_problems = []
        
        # Analisa sinal
        if 'signal' in data:
            all_problems.extend(self.analyze_signal_problems(data['signal']))
            
        # Analisa latência
        if 'latency' in data:
            all_problems.extend(self.analyze_latency_problems(data['latency']))
            
        # Analisa handovers
        if 'handover_history' in data:
            all_problems.extend(self.analyze_handover_problems(data['handover_history']))
            
        # Analisa cobertura
        if 'signal_history' in data:
            all_problems.extend(self.analyze_mesh_coverage(data['signal_history']))
            
        return all_problems

    def get_recommendations(self, problems):
        """Gera recomendações baseadas nos problemas encontrados"""
        recommendations = []
        
        if any(p['category'] == 'SIGNAL' for p in problems):
            recommendations.append({
                'priority': 'HIGH',
                'action': 'Otimização de Sinal',
                'steps': [
                    'Verifique obstáculos físicos',
                    'Considere reposicionar os pontos mesh',
                    'Verifique interferências de outras redes'
                ]
            })
            
        if any(p['category'] == 'HANDOVER' for p in problems):
            recommendations.append({
                'priority': 'MEDIUM',
                'action': 'Otimização de Handover',
                'steps': [
                    'Identifique áreas de transição',
                    'Ajuste posicionamento para melhor cobertura',
                    'Considere adicionar mais pontos mesh'
                ]
            })
            
        return recommendations

if __name__ == "__main__":
    # Exemplo de uso
    diagnostics = MeshDiagnostics()
    
    test_data = {
        'signal': -75,
        'latency': 120,
        'handover_history': [
            {'timestamp': datetime.now(), 'to_bssid': 'AA:BB:CC'},
            {'timestamp': datetime.now() - timedelta(minutes=1), 'to_bssid': 'DD:EE:FF'}
        ],
        'signal_history': [{'signal': -70}, {'signal': -75}]
    }
    
    problems = diagnostics.analyze_network_health(test_data)
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