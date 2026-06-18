from core.db import DataBase
from queries import categoria_queries

class CategoriaRepository:
    def get_all(self):
        db = DataBase()
        return db.execute(categoria_queries.QUERY_GET_ALL_CATEGORIAS, many=True)
