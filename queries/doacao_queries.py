QUERY_GET_DOACOES_PENDENTES = """
                                SELECT doador_id, data_solicitacao, status, observacao_vigilante FROM doacoes_solicitadas
                                WHERE
                                status = 'PENDENTE'
                              """

QUERY_CREATE_SOLICITACAO =  """
                            INSERT INTO doacoes_solicitadas (doador_id)
                            VALUES (%s)
                            RETURNING id
                            """

QUERY_CREATE_ITENS_SOLICITACAO = """
                                INSERT INTO itens_solicitacao(solicitacao_id, nome, quantidade, unidade_medida, data_vencimento, categoria_id)
                                VALUES (%s, %s, %s, %s, %s, %s)
                                """

QUERY_VALIDAR_DOACAO = """
                    UPDATE doacoes_solicitadas
                    SET status = 'APROVADA'
                    WHERE id = (%s)
                    RETURNING id;
                       """

QUERY_MOVER_ALIMENTOS_PARA_ESTOQUE ="""
                                    INSERT INTO alimentos(nome, categoria_id, quantidade, unidade_medida, data_vencimento)
                                    SELECT nome, categoria_id, quantidade, unidade_medida, data_vencimento
                                    FROM itens_solicitacao
                                    WHERE solicitacao_id = (%s)
                                    """

