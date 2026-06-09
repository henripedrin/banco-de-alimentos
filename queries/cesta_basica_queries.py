QUERY_CREATE_CESTA ="""
                    INSERT INTO cestas_basicas(nutricionista_id, recebedor_id)
                    VALUES (%s, %s)
                    RETURNING id
                    """

QUERY_UPDATE_ESTOQUE = """
                        UPDATE alimentos
                        SET quantidade = quantidade - (%s)
                        WHERE id = (%s) AND quantidade >= (%s)
                        RETURNING id
                        """

QUERY_INSERT_CESTA = """
                    INSERT INTO alimentos_cesta (cesta_id, alimento_id, quantidade_retirada)
                    VALUES (%s, %s, %s)
                    """