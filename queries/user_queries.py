# --- READ ---
QUERY_GET_ALL_USERS = "SELECT id, nome, username, categoria, ativo FROM usuarios ORDER BY id ASC;"
QUERY_GET_USER_BY_ID = "SELECT id, nome, username, categoria, ativo FROM usuarios WHERE id = %s;"
QUERY_GET_USER_BY_USERNAME = "SELECT * FROM usuarios WHERE username = %s;" # Usado pela autenticação
QUERY_COUNT_ADMINS = "SELECT COUNT(*) as total FROM usuarios WHERE categoria = 'ADMINISTRADOR' AND ativo = TRUE;"

# --- CREATE ---
QUERY_CREATE_USER = """
    INSERT INTO usuarios (nome, username, senha, categoria)
    VALUES (%s, %s, %s, %s)
    RETURNING id, nome, username, categoria, ativo;
"""

# --- UPDATE ---
# A query de atualização será construída dinamicamente no repositório
# para lidar com campos opcionais.

# --- DELETE ---
QUERY_DELETE_USER_BY_ID = "DELETE FROM usuarios WHERE id = %s RETURNING id;"
