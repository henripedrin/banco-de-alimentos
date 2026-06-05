from fastapi import APIRouter

import schemas
from services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Login"])

@router.post("/")
def login(username, password):
    authService = AuthService
    return authService.login(AuthService(), username, password)