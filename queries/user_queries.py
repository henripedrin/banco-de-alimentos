QUERY_GET_USER = """SELECT * FROM usuarios"""

QUERY_GET_USER_BY_USERNAME = """
                             SELECT * FROM usuarios
                             WHERE username = %s \
                             """

QUERY_CREATE_USER = """
                    INSERT INTO usuarios (name, username, senha, categoria)
                    VALUES (%s, %s, %s, %s)
                    RETURNING *
                    """

QUERY_UPDATE_USER = """
                    UPDATE usuarios
                    SET name = (%s)
                    WHERE username = (%s)
                    RETURNING id
                    """

QUERY_DELETE_USER = """
                    UPDATE usuarios 
                    SET ativo = FALSE
                    WHERE username = (%s)
                    RETURNING *
                    """