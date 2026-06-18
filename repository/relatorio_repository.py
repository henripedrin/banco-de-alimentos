from core.db import DataBase
from queries import relatorio_queries
from datetime import date

class RelatorioRepository:
    def save_report_metadata(self, file_name: str, reference_month: str, file_path: str):
        db = DataBase()
        return db.commit(relatorio_queries.QUERY_INSERT_RELATORIO, (file_name, reference_month, file_path))

    def get_all_reports(self):
        db = DataBase()
        return db.execute(relatorio_queries.QUERY_GET_ALL_RELATORIOS, many=True)

    def get_data_for_report(self, start_date: date, end_date: date):
        db = DataBase()
        
        doacoes = db.execute(relatorio_queries.QUERY_RELATORIO_DOACOES, (start_date, end_date), many=False)
        top_doadores = db.execute(relatorio_queries.QUERY_RELATORIO_TOP_DOADORES, (start_date, end_date), many=True)
        cestas = db.execute(relatorio_queries.QUERY_RELATORIO_CESTAS, (start_date, end_date), many=False)
        entregas = db.execute(relatorio_queries.QUERY_RELATORIO_ENTREGAS, (start_date, end_date), many=False)
        distribuidos = db.execute(relatorio_queries.QUERY_RELATORIO_ALIMENTOS_DISTRIBUIDOS, (start_date, end_date), many=False)
        recebidos = db.execute(relatorio_queries.QUERY_RELATORIO_ALIMENTOS_RECEBIDOS, (start_date, end_date), many=False)
        
        # O total de alimentos avariados precisa de uma query mais complexa,
        # por enquanto vamos retornar 0.
        
        return {
            "doacoes": doacoes,
            "top_doadores": top_doadores,
            "cestas": cestas,
            "entregas": entregas,
            "alimentos_distribuidos": distribuidos['total'] if distribuidos else 0,
            "alimentos_recebidos": recebidos['total'] if recebidos else 0,
            "alimentos_avariados": 0 # Placeholder
        }
