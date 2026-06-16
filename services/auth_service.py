from repository.user_repository import UserRepository
from core.security import verify_password, create_access_token
from fastapi import HTTPException, status
from passlib.exc import UnknownHashError
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AuthService:
    def __init__(self):
        self.user_repository = UserRepository()

    def authenticate_user(self, username: str, password: str):
        user_data = self.user_repository.get_by_username(username)
        if not user_data:
            logger.warning(f"Usuário não encontrado: {username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Nome de usuário ou senha incorretos",
            )

        password_ok = False
        try:
            # 1. Tenta verificar a senha como se fosse um hash (para usuários novos/atualizados)
            password_ok = verify_password(password, user_data['senha'])
        except UnknownHashError:
            # 2. Se falhar (porque é texto plano), tenta a comparação direta (para usuários do script SQL)
            logger.warning(f"A senha para o usuário '{username}' não é um hash. Tentando comparação de texto plano.")
            password_ok = (password == user_data['senha'])

        if not password_ok:
            logger.warning(f"Senha incorreta para o usuário: {username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Nome de usuário ou senha incorretos",
            )

        if not user_data['ativo']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuário inativo"
            )

        # 3. Gera o Token JWT
        access_token = create_access_token(data={"sub": user_data['username']})

        # 4. Retorna os dados para o frontend
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "profile": user_data['categoria'].lower()
        }
