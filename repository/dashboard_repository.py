from core.db import DataBase
from queries import dashboard_queries

class DashboardRepository:
    def get_admin_metrics(self):
        db = DataBase()

        users_by_category = db.execute(dashboard_queries.QUERY_COUNT_USERS_BY_CATEGORY, many=True)
        total_alimentos = db.execute(dashboard_queries.QUERY_COUNT_ALIMENTOS, many=False)
        total_doacoes = db.execute(dashboard_queries.QUERY_COUNT_DOACOES, many=False)
        total_cestas = db.execute(dashboard_queries.QUERY_COUNT_CESTAS, many=False)
        recent_activities = db.execute(dashboard_queries.QUERY_RECENT_ACTIVITIES, many=True)

        return {
            "users_by_category": users_by_category if users_by_category else [],
            "total_alimentos": total_alimentos['total'] if total_alimentos else 0,
            "total_doacoes": total_doacoes['total'] if total_doacoes else 0,
            "total_cestas": total_cestas['total'] if total_cestas else 0,
            "recent_activities": recent_activities if recent_activities else []
        }
