from core.db import DataBase
from queries import doacao_queries
from schemas.doacao_schema import DoacaoCreate


class DoacaoRepository:
    def get_doacoes_pendentes(self):
        db = DataBase()
        result = db.execute(doacao_queries.QUERY_GET_DOACOES_PENDENTES)
        if not result:
            return None
        return result

    def save_solicitacao(self, doacaoCreate: DoacaoCreate):
        db = DataBase()
        result_solicitacao = db.commit(doacao_queries.QUERY_CREATE_SOLICITACAO, (doacaoCreate.doador_nome,))
        solicitacao_id = result_solicitacao["id"]
        itens = []
        for alimento in doacaoCreate.itens_solicitacao:
            tupla_alimento = (
                solicitacao_id,
                alimento.nome,
                alimento.quantidade,
                alimento.unidade_medida,
                alimento.data_vencimento,
                alimento.categoria_id
            )
            itens.append(tupla_alimento)
        db.commit_many(doacao_queries.QUERY_CREATE_ITENS_SOLICITACAO, itens)

        return result_solicitacao

    def aceitar_doacao(self, solicitacao_id: int):
        db = DataBase()
        result = db.commit(doacao_queries.QUERY_VALIDAR_DOACAO, (solicitacao_id,))
        if not result:
            return None
        return result

    def mover_alimentos_para_estoque(self, solicitacao_id: int):
        db = DataBase()
        result = db.commit(doacao_queries.QUERY_MOVER_ALIMENTOS_PARA_ESTOQUE, (solicitacao_id,))
        if not result:
            return None
        return result