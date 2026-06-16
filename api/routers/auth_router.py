from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Login"])

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends()
):
    """
    Endpoint para autenticação de usuários.
    Recebe username e password em formato form-data (padrão OAuth2).
    """
    return auth_service.authenticate_user(form_data.username, form_data.password)
