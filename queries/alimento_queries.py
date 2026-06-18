QUERY_GET_FOOD = """SELECT * FROM alimentos
                    WHERE quantidade > 0"""

QUERY_GET_VALIDADE = """
    SELECT
        a.id,
        a.nome,
        c.nome as categoria_nome,
        a.quantidade,
        a.data_vencimento
    FROM alimentos a
    JOIN categorias c ON a.categoria_id = c.id
    WHERE a.quantidade > 0
    ORDER BY a.data_vencimento ASC;
"""

QUERY_INSERT_FOOD = """INSERT INTO alimentos (nome, categoria_id, quantidade, unidade_medida, data_vencimento)
                    VALUES (%s, %s, %s, %s, %s)"""
