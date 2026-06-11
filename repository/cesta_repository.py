from core.db import DataBase
from queries import cesta_basica_queries
from schemas.cesta_schema import CestaCreate, AlimentoCestaBase
from typing import List


class CestaRepository:

    def create_cesta_transactional(self, cesta_create: CestaCreate, alimentos: List[AlimentoCestaBase]):
        db = DataBase()
        with db.transaction() as cursor:
            # 1. Criar a cesta básica e obter o ID
            cursor.execute(cesta_basica_queries.QUERY_CREATE_CESTA, (cesta_create.nutricionista_id, cesta_create.recebedor_id))
            cesta_id = cursor.fetchone()['id']
            if not cesta_id:
                raise Exception("Falha ao criar a cesta.")

            # 2. Atualizar o estoque para cada alimento
            for alimento in alimentos:
                cursor.execute(cesta_basica_queries.QUERY_UPDATE_ESTOQUE, (alimento.quantidade_retirada, alimento.alimento_id, alimento.quantidade_retirada))
                if cursor.rowcount == 0:
                    raise Exception(f"Falha ao atualizar o estoque para o alimento_id: {alimento.alimento_id}. Quantidade insuficiente.")

            # 3. Inserir os alimentos na cesta
            alimentos_para_inserir = [(cesta_id, alimento.alimento_id, alimento.quantidade_retirada) for alimento in alimentos]
            cursor.executemany(cesta_basica_queries.QUERY_INSERT_CESTA, alimentos_para_inserir)

            return cesta_id
