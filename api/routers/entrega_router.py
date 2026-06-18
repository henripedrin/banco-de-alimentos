from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from schemas.entrega_schemas import EntregaPendenteResponse, EntregaDetalhesResponse
from services.entrega_service import EntregaService
from schemas.user_schemas import User
from api.dependencies import get_current_active_user

router = APIRouter(prefix="/entregas", tags=["Entregas"])

@router.get("/pendentes", response_model=List[EntregaPendenteResponse])
def get_entregas_pendentes(
    service: EntregaService = Depends(),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retorna uma lista de todas as entregas com status 'PENDENTE'.
    Acesso restrito para Operadores Logísticos.
    """
    if current_user.categoria != "OPERADOR_LOGISTICO":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado.")
    return service.get_entregas_pendentes()

@router.get("/{entrega_id}/detalhes", response_model=EntregaDetalhesResponse)
def get_entrega_detalhes(
    entrega_id: int,
    service: EntregaService = Depends(),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retorna os detalhes de uma entrega específica, incluindo os itens da cesta.
    Acesso restrito para Operadores Logísticos.
    """
    if current_user.categoria != "OPERADOR_LOGISTICO":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado.")
    return service.get_entrega_detalhes(entrega_id)

@router.put("/{entrega_id}/confirmar")
def confirmar_entrega(
    entrega_id: int,
    service: EntregaService = Depends(),
    current_user: User = Depends(get_current_active_user)
):
    """
    Confirma a realização de uma entrega.
    Acesso restrito para Operadores Logísticos.
    """
    if current_user.categoria != "OPERADOR_LOGISTICO":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado.")
    return service.confirmar_entrega(entrega_id, current_user.id)
