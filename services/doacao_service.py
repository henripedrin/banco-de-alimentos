from repository.doacao_repository import DoacaoRepository
from schemas.doacao_schema import DoacaoCreate, DoacaoHistoryResponse, ItemDoacao, DoacaoDetalhesResponse, ItemDoacaoDetalhes, DoacaoPendente
from fastapi import HTTPException, status
from typing import List

class DoacaoService:
    def __init__(self):
        self.repository = DoacaoRepository()

    def get_doacoes_for_current_user(self, doador_id: int) -> List[DoacaoHistoryResponse]:
        solicitacoes = self.repository.get_doacoes_by_doador_id(doador_id)
        if not solicitacoes:
            return []
        solicitacao_ids = [s['id'] for s in solicitacoes]
        itens = self.repository.get_itens_for_solicitacoes(solicitacao_ids)
        itens_map = {}
        for item in itens:
            sol_id = item['solicitacao_id']
            if sol_id not in itens_map:
                itens_map[sol_id] = []
            itens_map[sol_id].append(ItemDoacao(**item))
        response = []
        for sol in solicitacoes:
            sol_id = sol['id']
            response.append(
                DoacaoHistoryResponse(
                    id=sol_id,
                    data_solicitacao=sol['data_solicitacao'],
                    status=sol['status'],
                    observacao_vigilante=sol['observacao_vigilante'],
                    itens=itens_map.get(sol_id, [])
                )
            )
        return response

    def create_solicitacao_for_current_user(self, doador_id: int, doacao_create: DoacaoCreate):
        for item in doacao_create.itens_solicitacao:
            if item.possui_avaria:
                if not item.quantidade_avariada or item.quantidade_avariada <= 0:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Para o item '{item.nome}', a quantidade avariada deve ser informada e maior que zero.")
                if not item.descricao_avaria:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Para o item '{item.nome}', a descrição da avaria é obrigatória.")
                if item.quantidade_avariada > item.quantidade:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Para o item '{item.nome}', a quantidade avariada não pode ser maior que a quantidade total.")
        solicitacao_id = self.repository.save_solicitacao_transacional(doador_id, doacao_create)
        return {"id": solicitacao_id}

    def get_doacoes_pendentes(self) -> List[DoacaoPendente]:
        return self.repository.get_doacoes_pendentes_com_doador()

    def get_doacao_detalhes(self, solicitacao_id: int) -> DoacaoDetalhesResponse:
        detalhes = self.repository.get_detalhes_doacao(solicitacao_id)
        if not detalhes:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doação não encontrada.")
        return detalhes

    def aprovar_doacao(self, solicitacao_id: int):
        return self.repository.aprovar_doacao(solicitacao_id)

    def rejeitar_doacao(self, solicitacao_id: int, motivo: str):
        result = self.repository.rejeitar_doacao(solicitacao_id, motivo)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doação não encontrada.")
        return {"id": solicitacao_id, "status": "REJEITADA"}
