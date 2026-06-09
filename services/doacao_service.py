from repository.doacao_repository import DoacaoRepository
from schemas.doacao_schema import DoacaoCreate


class DoacaoService:
    def get_doacoes_pendentes(self):
        doacaoRepository = DoacaoRepository()
        return doacaoRepository.get_doacoes_pendentes()

    def create_solicitacao(self, doacaoCreate: DoacaoCreate):
        doacaoRepository = DoacaoRepository()
        return doacaoRepository.save_solicitacao(doacaoCreate)

    def aceitar_doacao(self, solicitacao_id: int):
        doacaoRepository = DoacaoRepository()
        result = doacaoRepository.aceitar_doacao(solicitacao_id)
        if result is None:
            return None
        doacaoRepository.mover_alimentos_para_estoque(solicitacao_id)
        return result