from fastapi import APIRouter, Depends
from typing import List
from services.categoria_service import CategoriaService
from schemas.categoria_schema import Categoria
from api.dependencies import get_current_active_user

router = APIRouter(prefix="/categorias", tags=["Categorias"])

@router.get("/", response_model=List[Categoria])
def get_all_categorias(
    service: CategoriaService = Depends(),
    current_user: dict = Depends(get_current_active_user)
):
    """
    Retorna todas as categorias de alimentos cadastradas.
    """
    return service.get_all_categorias()
