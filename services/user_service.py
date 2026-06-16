from repository.user_repository import UserRepository
from schemas.user_schemas import UserCreate, UserUpdate
from core.security import get_password_hash
from fastapi import HTTPException, status

class UserService:
    def __init__(self):
        self.repository = UserRepository()

    def get_all_users(self):
        return self.repository.get_all()

    def get_user_by_id(self, user_id: int):
        user = self.repository.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        return user

    def create_user(self, user_create: UserCreate):
        # 1. Verifica se o username já existe
        existing_user = self.repository.get_by_username(user_create.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="O nome de usuário já está em uso."
            )

        # 2. Faz o hash da senha antes de salvar
        hashed_password = get_password_hash(user_create.senha)
        user_create.senha = hashed_password

        # 3. Salva no banco
        return self.repository.create(user_create)

    def update_user(self, user_id: int, user_update: UserUpdate):
        # 1. Verifica se o usuário a ser atualizado existe
        user_db = self.repository.get_by_id(user_id)
        if not user_db:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        # 2. Se um novo username foi fornecido, verifica se ele já não está em uso por outro usuário
        if user_update.username and user_update.username != user_db['username']:
            existing_user = self.repository.get_by_username(user_update.username)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="O novo nome de usuário já está em uso."
                )

        # 3. Se uma nova senha foi fornecida, faz o hash dela
        if user_update.senha:
            user_update.senha = get_password_hash(user_update.senha)

        # 4. Atualiza no banco
        return self.repository.update(user_id, user_update)

    def delete_user(self, user_id: int):
        # 1. Verifica se o usuário a ser deletado existe
        user_to_delete = self.repository.get_by_id(user_id)
        if not user_to_delete:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        # 2. Regra de negócio: não permitir exclusão do último administrador
        if user_to_delete['categoria'] == 'ADMINISTRADOR':
            admin_count = self.repository.count_admins()
            if admin_count <= 1:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Não é possível excluir o último administrador do sistema."
                )

        # 3. Deleta do banco
        deleted = self.repository.delete(user_id)
        if not deleted:
            raise HTTPException(status_code=500, detail="Falha ao excluir o usuário.")
        return {"message": "Usuário excluído com sucesso", "user_id": user_id}
