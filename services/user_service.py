from fastapi import HTTPException

from repository.user_repository import UserRepository
from schemas.user_schemas import UserCreate, UserUpdate


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
            if userCreate.username.strip() == "" or userCreate.senha.strip() == "" or userCreate.categoria.strip() == "" or userCreate.nome.strip() == "":
                raise ValueError
            return userRepository.save(userCreate)
        except ValueError:
            raise HTTPException(status_code=400, detail="Campos vazios não são permitidos")
        except FileExistsError:
            raise HTTPException(status_code=409, detail="Usuário já existe")

    def update_user(self, userUpdate: UserUpdate, username: str):
        try:
            userRepository = UserRepository()
            print(username.strip())
            print(userUpdate.nome.strip())
            if userRepository.get_by_username(username) is None:
                raise FileNotFoundError
            if userUpdate.nome.strip() == "" or username.strip() == "":
                raise ValueError
            if userRepository.get_by_username(username).nome == userUpdate.nome:
                raise FileExistsError
            userRepository.put(userUpdate, username)
            return {"mensagem": "Usuário atualizado com sucesso!"}
        except ValueError as e:
            import traceback
            print("====== TRACEBACK DO ERRO 400 ======")
            traceback.print_exc()
            print("====================================")
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        except FileExistsError:
            raise HTTPException(status_code=409, detail="O usuário já possui esse nome")

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

