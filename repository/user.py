from core.db import DataBase
from schemas.user import User


class UserRepository:
    QUERY_GET_USER = """SELECT * FROM usuarios"""

    QUERY_GET_USER_BY_USERNAME = """
    SELECT * FROM usuarios
    WHERE username = %s
    """

    def get_by_username(self, username):
        db = DataBase()
        rows = db.execute(self.QUERY_GET_USER_BY_USERNAME, (username,))
        if not rows:
            return None
        row = rows[0]
        return User(id=row[0], name=row[1], username=row[2], senha=row[3])

    def get_credentials(self, username):
        db = DataBase()
        print("======== LENDO O ARQUIVO NOVO ========")
        rows = db.execute(self.QUERY_GET_USER_BY_USERNAME, (username,))
        if not rows:
            return None
        row = rows[0]
        return [row[2], row[3]]
