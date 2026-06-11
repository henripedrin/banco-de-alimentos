from core.db import DataBase
from schemas.user_schemas import User, UserUpdate, UserCreate
from queries import user_queries

class UserRepository:
    def get_by_username(self, username: str):
        db = DataBase()
        results = db.execute(user_queries.QUERY_GET_USER_BY_USERNAME, (username,))
        if not results:
            return None
        result = results[0]
        return User(id=result["id"],
                    nome=result["nome"],
                    username=result["username"],
                    senha=result["senha"],
                    categoria=result["categoria"],
                    ativo=result["ativo"])

    def get_credentials(self, username: str):
        db = DataBase()
        rows = db.execute(user_queries.QUERY_GET_USER_BY_USERNAME, (username,))
        if not rows:
            return None
        row = rows[0]
        return [row['username'], row['senha']]

    def save(self, userCreate: UserCreate):
        db = DataBase()
        result = db.commit(user_queries.QUERY_CREATE_USER, (userCreate.nome, userCreate.username, userCreate.senha, userCreate.categoria))
        if result:
            return User(id=result["id"],
                        nome=result["nome"],
                        username=result["username"],
                        senha=result["senha"],
                        categoria=result["categoria"],
                        ativo=result["ativo"])
        return None

    def put(self, userUpdate: UserUpdate, username: str):
        db = DataBase()
        result = db.commit(user_queries.QUERY_UPDATE_USER, (userUpdate.nome, username))
        if result:
            return UserUpdate(nome=userUpdate.nome)
        return None

    def delete(self, username: str):
        db = DataBase()
        result = db.commit(user_queries.QUERY_DELETE_USER, (username,))
        if not result:
            return None
        return User(id=result["id"],
                    nome=result["nome"],
                    username=result["username"],
                    senha=result["senha"],
                    categoria=result["categoria"],
                    ativo=result["ativo"])

    def get_all(self):
        db = DataBase()
        rows = db.execute(user_queries.QUERY_GET_USER)
        if not rows:
            return None
        return rows
