from fastapi import APIRouter

import schemas
from services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Login"])

@router.post("/", response_model=list)
def login(username, password):
    authService = AuthService
    return authService.login(AuthService(), username, password)