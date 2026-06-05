from fastapi import HTTPException

from repository.user_repository import UserRepository
from schemas.user import UserCreate, UserUpdate


class UserService:
    def get_users(self):
        try:
            userRepository = UserRepository()
            result = userRepository.get_all()
            if result is None:
                raise ValueError
            return result
        except ValueError:
            raise HTTPException(status_code=404, detail="Nenhum usuário encontrado")

    def get_user_by_username(self, username):
        try:
            userRepository = UserRepository()
            result = userRepository.get_by_username(username)
            if result is None:
                raise ValueError
            return result
        except ValueError:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

    def create_user(self, userCreate: UserCreate):
        try:
            userRepository = UserRepository()
            if userRepository.get_by_username(userCreate.username):
                raise FileExistsError
            if userCreate.username.strip() == "" or userCreate.senha.strip() == "" or userCreate.categoria.strip() == "" or userCreate.name.strip() == "":
                raise ValueError
            return userRepository.save(userCreate)
        except ValueError:
            raise HTTPException(status_code=400, detail="Campos vazios não são permitidos")
        except FileExistsError:
            raise HTTPException(status_code=409, detail="Usuário já existe")

    def update_user(self, userUpdate: UserUpdate, username):
        try:
            userRepository = UserRepository()
            if userRepository.get_by_username(username) is None:
                raise FileNotFoundError
            if userUpdate.name.strip() == "" or username.strip() == "":
                raise ValueError
            return userRepository.put(userUpdate, username)
        except ValueError:
            raise HTTPException(status_code=400, detail="Campos vazios não são permitidos")
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

    def delete_user(self, username):
        try:
            userRepository = UserRepository()
            if userRepository.get_by_username(username) is None:
                raise FileNotFoundError
            if username.strip() == "":
                raise ValueError("Campo vazio não é permitido")
            if userRepository.get_by_username(username).ativo == False:
                raise ValueError("Usuário já deletado")
            return userRepository.delete(username)
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

