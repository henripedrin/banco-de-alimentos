from core.db import DataBase
from queries import doacao_queries
from schemas.doacao_schema import DoacaoCreate
from typing import List

class DoacaoRepository:
    def get_doacoes_by_doador_id(self, doador_id: int):
        db = DataBase()
        return db.execute(doacao_queries.QUERY_GET_DOACOES_BY_DOADOR_ID, (doador_id,), many=True)

    def get_itens_for_solicitacoes(self, solicitacao_ids: List[int]):
        if not solicitacao_ids:
            return []
        db = DataBase()
        return db.execute(doacao_queries.QUERY_GET_ITENS_BY_SOLICITACAO_IDS, (solicitacao_ids,), many=True)

    def save_solicitacao_transacional(self, doador_id: int, doacao_create: DoacaoCreate):
        db = DataBase()
        with db.transaction() as cursor:
            cursor.execute(doacao_queries.QUERY_CREATE_SOLICITACAO, (doador_id,))
            solicitacao_id = cursor.fetchone()['id']
            if not solicitacao_id:
                raise Exception("Falha ao criar a solicitação de doação.")

            for item in doacao_create.itens_solicitacao:
                cursor.execute(
                    doacao_queries.QUERY_CREATE_ITENS_SOLICITACAO,
                    (
                        solicitacao_id,
                        item.nome,
                        item.quantidade,
                        item.unidade_medida,
                        item.data_vencimento,
                        item.categoria_id
                    )
                )
                item_inserido = cursor.fetchone()
                if not item_inserido:
                    raise Exception(f"Falha ao inserir o item '{item.nome}' na solicitação.")

                item_solicitacao_id = item_inserido['id']

                if item.possui_avaria and item.quantidade_avariada > 0:
                    cursor.execute(
                        doacao_queries.QUERY_INSERT_ALIMENTO_AVARIADO,
                        (
                            item_solicitacao_id,
                            item.quantidade_avariada,
                            item.descricao_avaria
                        )
                    )

            return solicitacao_id

    def get_doacoes_pendentes_com_doador(self):
        db = DataBase()
        return db.execute(doacao_queries.QUERY_GET_DOACOES_PENDENTES, many=True)

    def get_detalhes_doacao(self, solicitacao_id: int):
        db = DataBase()
        doacao = db.execute(doacao_queries.QUERY_GET_DOACAO_DETALHES, (solicitacao_id,), many=False)
        if not doacao:
            return None
        itens = db.execute(doacao_queries.QUERY_GET_ITENS_DETALHES_BY_SOLICITACAO_ID, (solicitacao_id,), many=True)
        doacao['itens'] = itens if itens else []
        return doacao

    def aprovar_doacao(self, solicitacao_id: int):
        db = DataBase()
        # Envolve a aprovação e a movimentação para estoque em uma transação
        with db.transaction() as cursor:
            cursor.execute(doacao_queries.QUERY_APROVAR_DOACAO, (solicitacao_id,))
            if cursor.rowcount == 0:
                raise Exception("Doação não encontrada ou já processada.")

            cursor.execute(doacao_queries.QUERY_MOVER_ALIMENTOS_PARA_ESTOQUE, (solicitacao_id,))
        return {"id": solicitacao_id, "status": "APROVADA"}

    def rejeitar_doacao(self, solicitacao_id: int, motivo: str):
        db = DataBase()
        result = db.commit(doacao_queries.QUERY_REJEITAR_DOACAO, (motivo, solicitacao_id))
        return result
