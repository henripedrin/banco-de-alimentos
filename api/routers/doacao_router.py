from fastapi import APIRouter

from schemas.doacao_schema import DoacaoResponse, DoacaoCreate, DoacaoSucessoResponse
from services.doacao_service import DoacaoService

router = APIRouter(prefix="/doador", tags=["Doador"])

@router.get("/", response_model=list[DoacaoResponse])
def get_solicitacoes_pendentes():
    doacaoService = DoacaoService()
    return doacaoService.get_doacoes_pendentes()

@router.post("/", response_model=DoacaoSucessoResponse)
def create_solicitacao(doacaoCreate: DoacaoCreate):
    doacaoService = DoacaoService()
    result = doacaoService.create_solicitacao(doacaoCreate)
    return DoacaoSucessoResponse(
        mensagem="Doação registrada com sucesso!",
        solicitacao_id=result["id"])

@router.put("/{solicitacao_id}")
def aceitar_doacao(solicitacao_id: int):
    doacaoService = DoacaoService()
    result = doacaoService.aceitar_doacao(solicitacao_id)
    return result