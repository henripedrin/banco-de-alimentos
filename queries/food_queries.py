QUERY_GET_FOOD = """SELECT * FROM alimentos
                    WHERE quantidade > 0"""

QUERY_GET_VALIDADE = """SELECT name, quantidade, data_vencimento
                        FROM alimentos
                        WHERE quantidade > 0
                        ORDER BY data_vencimento ASC"""