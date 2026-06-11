
from core.db import DataBase
from queries import alimento_queries
from schemas.alimento_schemas import LoteCreate


class FoodRepository:
    def get_validade(self):
        db = DataBase()
        result = db.execute(alimento_queries.QUERY_GET_VALIDADE)
        if not result:
            return None
        return result

    def save_food(self, lote: LoteCreate):
        db = DataBase
        parameters = []
        for food in lote.alimentos:
            tuple_alimento = (
                (food.name, food.quantidade, food.categoria_id, food.quantidade, food.unidade_medida, food.data_vencimento))
            parameters.append(tuple_alimento)
        rows = db.commit_many(alimento_queries.QUERY_INSERT_FOOD, parameters)
        if not rows:
            return None
        return rows