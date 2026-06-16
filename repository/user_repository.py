from core.db import DataBase
from schemas.user_schemas import UserCreate, UserUpdate, User
from queries import user_queries

class UserRepository:
    def get_all(self):
        db = DataBase()
        rows = db.execute(user_queries.QUERY_GET_ALL_USERS, many=True)
        return rows if rows else []

    def get_by_id(self, user_id: int):
        db = DataBase()
        result = db.execute(user_queries.QUERY_GET_USER_BY_ID, (user_id,), many=False)
        return result

    def get_by_username(self, username: str):
        db = DataBase()
        result = db.execute(user_queries.QUERY_GET_USER_BY_USERNAME, (username,), many=False)
        return result

    def create(self, user: UserCreate):
        db = DataBase()
        result = db.commit(user_queries.QUERY_CREATE_USER, (user.nome, user.username, user.senha, user.categoria))
        return result

    def update(self, user_id: int, user_update: UserUpdate):
        # Constrói a query de update dinamicamente com base nos campos fornecidos
        set_clauses = []
        params = []

        update_data = user_update.dict(exclude_unset=True)
        if not update_data:
            return None # Nenhum dado para atualizar

        for key, value in update_data.items():
            set_clauses.append(f"{key} = %s")
            params.append(value)

        set_clause_str = ", ".join(set_clauses)
        params.append(user_id) # Adiciona o ID ao final para a cláusula WHERE

        query = f"UPDATE usuarios SET {set_clause_str} WHERE id = %s RETURNING id, nome, username, categoria, ativo;"

        db = DataBase()
        result = db.commit(query, tuple(params))
        return result

    def delete(self, user_id: int):
        db = DataBase()
        result = db.commit(user_queries.QUERY_DELETE_USER_BY_ID, (user_id,))
        return result

    def count_admins(self):
        db = DataBase()
        result = db.execute(user_queries.QUERY_COUNT_ADMINS, many=False)
        return result['total'] if result else 0
