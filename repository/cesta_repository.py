from core.db import DataBase
from queries import cesta_basica_queries
from schemas.cesta_schema import AlimentoCestaCreate, ListaAlimentosCestaCreate


class CestaRepository:
    def save_cesta(self, nutricionista_id, recebedor_id):
        db = DataBase()
        cesta = db.commit(cesta_basica_queries.QUERY_CREATE_CESTA, (nutricionista_id, recebedor_id))
        if not cesta:
            return None
        return cesta

    def update_estoque(self, alimentoCestaCreate: AlimentoCestaCreate):
        db = DataBase()
        result = db.commit(cesta_basica_queries.QUERY_UPDATE_ESTOQUE, (alimentoCestaCreate.quantidade_retirada, alimentoCestaCreate.alimento_id, alimentoCestaCreate.quantidade_retirada))
        if not result:
            return None
        return result

    def insert_alimentos(self, listaAlimentosCestaCreate: ListaAlimentosCestaCreate):
        db = DataBase()
        parameters = []
        for alimento in listaAlimentosCestaCreate.alimentos:
            tuple_alimento = (alimento.cesta_id, alimento.alimento_id, alimento.quantidade_retirada)
            parameters.append(tuple_alimento)
        rows = db.commit_many(cesta_basica_queries.QUERY_INSERT_CESTA, parameters)
        if not rows:
            return None
        return rows