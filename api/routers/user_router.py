from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from schemas.user_schemas import UserCreate, UserUpdate, User
from services.user_service import UserService
from api.dependencies import get_current_active_user
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/usuarios", tags=["Usuários"])

@router.get("/", response_model=List[User])
def get_users(
    service: UserService = Depends(),
    current_user: dict = Depends(get_current_active_user)
):
    """
    Retorna uma lista com todos os usuários cadastrados.
    Requer autenticação.
    """
    return service.get_all_users()

@router.get("/{user_id}", response_model=User)
def get_user(
    user_id: int,
    service: UserService = Depends(),
    current_user: dict = Depends(get_current_active_user)
):
    """
    Retorna os detalhes de um usuário específico pelo ID.
    Requer autenticação.
    """
    return service.get_user_by_id(user_id)

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserCreate,
    service: UserService = Depends(),
    current_user: dict = Depends(get_current_active_user)
):
    """
    Cadastra um novo usuário no sistema.
    Requer autenticação (apenas admins, idealmente, mas o request não restringiu o nível de permissão aqui, apenas o dashboard. Vou manter protegido de forma geral).
    """
    try:
        return service.create_user(user)
    except Exception as e:
        logger.error(f"Erro ao criar usuário: {e}")
        # Se não for uma HTTPException (lançada pelo service), lança um erro 500
        if not isinstance(e, HTTPException):
            raise HTTPException(status_code=500, detail="Erro interno no servidor ao criar usuário")
        raise e

@router.put("/{user_id}", response_model=User)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    service: UserService = Depends(),
    current_user: dict = Depends(get_current_active_user)
):
    """
    Atualiza os dados de um usuário existente.
    Requer autenticação.
    """
    try:
        return service.update_user(user_id, user_update)
    except Exception as e:
        logger.error(f"Erro ao atualizar usuário {user_id}: {e}")
        if not isinstance(e, HTTPException):
            raise HTTPException(status_code=500, detail="Erro interno no servidor ao atualizar usuário")
        raise e

@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(
    user_id: int,
    service: UserService = Depends(),
    current_user: dict = Depends(get_current_active_user)
):
    """
    Exclui um usuário do sistema (Hard Delete).
    Requer autenticação.
    """
    try:
        return service.delete_user(user_id)
    except Exception as e:
        logger.error(f"Erro ao excluir usuário {user_id}: {e}")
        if not isinstance(e, HTTPException):
            raise HTTPException(status_code=500, detail="Erro interno no servidor ao excluir usuário")
        raise e
