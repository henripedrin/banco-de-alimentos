from fastapi import APIRouter

from services.alimento_service import AlimentoService
from schemas.alimento_schemas import AlimentoResponse

router = APIRouter(prefix="/admin_index", tags=["admin_index"])

@router.get("/", response_model=list[AlimentoResponse])
def get_validade():
    foodService = AlimentoService()
    return foodService.get_validade()