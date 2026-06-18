from repository.dashboard_repository import DashboardRepository

class DashboardService:
    def __init__(self):
        self.repository = DashboardRepository()

    def get_admin_dashboard_data(self):
        metrics = self.repository.get_admin_metrics()
        
        user_counts = {item['categoria'].upper(): item['total'] for item in metrics['users_by_category']}
        total_users = sum(user_counts.values())

        processed_metrics = {
            "total_users": total_users,
            "total_doadores": user_counts.get('DOADOR', 0),
            "total_recebedores": user_counts.get('RECEBEDOR', 0),
            "total_nutricionistas": user_counts.get('NUTRICIONISTA', 0),
            "total_agentes_sanitarios": user_counts.get('AGENTE_SANITARIO', 0),
            "total_operadores_logisticos": user_counts.get('OPERADOR_LOGISTICO', 0),
            "total_alimentos": metrics['total_alimentos'],
            "total_doacoes": metrics['total_doacoes'],
            "total_cestas": metrics['total_cestas'],
            "recent_activities": metrics['recent_activities']
        }
        
        return processed_metrics

    def get_logistica_dashboard_data(self):
        metrics = self.repository.get_logistica_metrics()
        
        status_counts = {item['status'].upper(): item['total'] for item in metrics['entregas_by_status']}

        # Para o card "Transportes em andamento", vamos considerar as 'PENDENTE'
        processed_metrics = {
            "entregas_pendentes": status_counts.get('PENDENTE', 0),
            "entregas_concluidas": status_counts.get('ENTREGUE', 0),
            "transportes_em_andamento": status_counts.get('PENDENTE', 0),
            "ultimas_entregas": metrics['ultimas_entregas']
        }

        return processed_metrics
