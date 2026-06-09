QUERY_GET_FOOD = """SELECT * FROM alimentos
                    WHERE quantidade > 0"""

QUERY_GET_VALIDADE = """SELECT nome, quantidade, data_vencimento
                        FROM alimentos
                        WHERE quantidade > 0
                        ORDER BY data_vencimento ASC"""

QUERY_INSERT_FOOD = """INSERT INTO alimentos (nome, categoria_id, quantidade, unidade_medida, data_vencimento)
                    VALUES (%s, %s, %s, %s, %s)"""