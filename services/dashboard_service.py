from repository.dashboard_repository import DashboardRepository

class DashboardService:
    def __init__(self):
        self.repository = DashboardRepository()

    def get_admin_dashboard_data(self):
        metrics = self.repository.get_admin_metrics()

        # Processar os dados para um formato mais amigável para o frontend
        user_counts = {item['categoria'].upper(): item['total'] for item in metrics['users_by_category']}

        total_users = sum(user_counts.values())

        # O frontend espera os totais de cada perfil
        processed_metrics = {
            "total_users": total_users,
            "total_doadores": user_counts.get('DOADOR', 0),
            "total_recebedores": user_counts.get('RECEBEDOR', 0),
            "total_nutricionistas": user_counts.get('NUTRICIONISTA', 0),
            "total_agentes_sanitarios": user_counts.get('AGENTE_SANITARIO', 0),
            "total_operadores_logisticos": user_counts.get('OPERADOR_LOGISTICO', 0),
            "total_alimentos": metrics['total_alimentos'],
            "total_doacoes": metrics['total_doacoes'], # Renomeado de lotes para doações
            "total_cestas": metrics['total_cestas'],
            "recent_activities": metrics['recent_activities']
        }

        return processed_metrics
