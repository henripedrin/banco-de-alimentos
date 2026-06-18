from fastapi import APIRouter, Depends, HTTPException, status
from schemas.doacao_schema import DoacaoCreate, DoacaoSucessoResponse, DoacaoHistoryResponse, DoacaoPendente, DoacaoDetalhesResponse, DoacaoRejeitar
from services.doacao_service import DoacaoService
from schemas.user_schemas import User
from api.dependencies import get_current_active_user
from typing import List

router = APIRouter(prefix="/doacoes", tags=["Doações"])

# --- Endpoints para DOADOR ---

@router.get("/me", response_model=List[DoacaoHistoryResponse])
def get_my_donations(
    current_user: User = Depends(get_current_active_user),
    service: DoacaoService = Depends()
):
    if current_user.categoria != "DOADOR":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado.")
    return service.get_doacoes_for_current_user(current_user.id)

@router.post("/", response_model=DoacaoSucessoResponse, status_code=status.HTTP_201_CREATED)
def create_new_donation(
    doacao_create: DoacaoCreate,
    current_user: User = Depends(get_current_active_user),
    service: DoacaoService = Depends()
):
    if current_user.categoria != "DOADOR":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado.")
    result = service.create_solicitacao_for_current_user(current_user.id, doacao_create)
    return DoacaoSucessoResponse(
        mensagem="Sua doação foi registrada com sucesso e será verificada em breve. Muito obrigado!",
        solicitacao_id=result["id"]
    )

# --- Endpoints para AGENTE SANITÁRIO ---

@router.get("/pendentes", response_model=List[DoacaoPendente])
def get_pendent_donations(
    current_user: User = Depends(get_current_active_user),
    service: DoacaoService = Depends()
):
    if current_user.categoria != "AGENTE_SANITARIO":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado.")
    return service.get_doacoes_pendentes()

@router.get("/{doacao_id}/detalhes", response_model=DoacaoDetalhesResponse)
def get_donation_details(
    doacao_id: int,
    current_user: User = Depends(get_current_active_user),
    service: DoacaoService = Depends()
):
    if current_user.categoria != "AGENTE_SANITARIO":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado.")
    return service.get_doacao_detalhes(doacao_id)

@router.put("/{doacao_id}/aprovar")
def approve_donation(
    doacao_id: int,
    current_user: User = Depends(get_current_active_user),
    service: DoacaoService = Depends()
):
    if current_user.categoria != "AGENTE_SANITARIO":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado.")
    return service.aprovar_doacao(doacao_id)

@router.put("/{doacao_id}/rejeitar")
def reject_donation(
    doacao_id: int,
    rejeicao: DoacaoRejeitar,
    current_user: User = Depends(get_current_active_user),
    service: DoacaoService = Depends()
):
    if current_user.categoria != "AGENTE_SANITARIO":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado.")
    return service.rejeitar_doacao(doacao_id, rejeicao.motivo)
