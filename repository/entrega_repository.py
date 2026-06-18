from core.db import DataBase
from queries import entrega_queries

class EntregaRepository:
    def get_entregas_pendentes(self):
        db = DataBase()
        return db.execute(entrega_queries.QUERY_GET_ENTREGAS_PENDENTES, many=True)

    def get_entrega_by_id(self, entrega_id: int):
        db = DataBase()
        return db.execute(entrega_queries.QUERY_GET_ENTREGA_DETALHES, (entrega_id,), many=False)

    def get_alimentos_by_cesta_id(self, cesta_id: int):
        db = DataBase()
        return db.execute(entrega_queries.QUERY_GET_ALIMENTOS_CESTA, (cesta_id,), many=True)

    def confirmar_entrega(self, entrega_id: int, operador_id: int):
        db = DataBase()
        result = db.commit(entrega_queries.QUERY_CONFIRMAR_ENTREGA, (operador_id, entrega_id))
        return result
