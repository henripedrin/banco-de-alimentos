from core.db import DataBase
from queries import food_queries


class FoodRepository:
    def get_validade(self):
        db = DataBase()
        result = db.execute(food_queries.QUERY_GET_VALIDADE)
        if not result:
            return None
        return result