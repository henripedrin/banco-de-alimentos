from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from services.alimento_service import AlimentoService
from schemas.alimento_schemas import AlimentoResponse
from schemas.user_schemas import User
from api.dependencies import get_current_active_user

router = APIRouter(prefix="/alimentos", tags=["Alimentos"])

@router.get("/validade", response_model=List[AlimentoResponse])
def get_validade(
    service: AlimentoService = Depends(),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retorna uma lista de todos os alimentos com quantidade > 0,
    ordenados por data de vencimento.
    Acesso restrito para Nutricionistas.
    """
    if current_user.categoria != "NUTRICIONISTA":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Apenas para nutricionistas."
        )
    return service.get_validade()
