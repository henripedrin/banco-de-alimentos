from fastapi import APIRouter, Depends, HTTPException
from schemas.cesta_schema import CestaRequest
from services.cesta_service import CestaService
import logging

router = APIRouter(prefix="/cestas", tags=["Cestas"])

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/", status_code=201)
def create_cesta_endpoint(
    request: CestaRequest,
    service: CestaService = Depends()
):
    """
    Cria uma nova cesta básica de forma transacional.

    - **cesta**: Informações da cesta (nutricionista e recebedor).
    - **alimentos**: Lista de alimentos a serem incluídos na cesta.
    """
    try:
        result = service.create_cesta(request)
        return result
    except Exception as e:
        logger.error(f"Erro no endpoint de criação de cesta: {e}")
        raise HTTPException(status_code=400, detail=str(e))
