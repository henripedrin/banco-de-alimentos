# --- READ ---
QUERY_GET_DOACOES_BY_DOADOR_ID = """
    SELECT id, data_solicitacao, status, observacao_vigilante
    FROM doacoes_solicitadas
    WHERE doador_id = %s
    ORDER BY data_solicitacao DESC;
"""
QUERY_GET_ITENS_BY_SOLICITACAO_IDS = """
    SELECT solicitacao_id, nome, quantidade, unidade_medida
    FROM itens_solicitacao
    WHERE solicitacao_id = ANY(%s);
"""
QUERY_GET_DOACOES_PENDENTES = """
    SELECT ds.id, ds.data_solicitacao, ds.status, u.nome as doador_nome
    FROM doacoes_solicitadas ds
    JOIN usuarios u ON ds.doador_id = u.id
    WHERE ds.status = 'PENDENTE'
    ORDER BY ds.data_solicitacao ASC;
"""
QUERY_GET_DOACAO_DETALHES = """
    SELECT
        ds.id, ds.data_solicitacao, ds.status, ds.observacao_vigilante, u.nome as doador_nome
    FROM doacoes_solicitadas ds
    JOIN usuarios u ON ds.doador_id = u.id
    WHERE ds.id = %s;
"""
QUERY_GET_ITENS_DETALHES_BY_SOLICITACAO_ID = """
    SELECT
        its.id, its.nome, its.quantidade, its.unidade_medida, its.data_vencimento,
        its.categoria_id,
        av.quantidade as quantidade_avariada, av.descricao as descricao_avaria
    FROM itens_solicitacao its
    LEFT JOIN alimentos_avariados av ON its.id = av.alimento_id
    WHERE its.solicitacao_id = %s;
"""

# --- CREATE ---
QUERY_CREATE_SOLICITACAO =  """
    INSERT INTO doacoes_solicitadas (doador_id)
    VALUES (%s)
    RETURNING id;
"""
QUERY_CREATE_ITENS_SOLICITACAO = """
    INSERT INTO itens_solicitacao(solicitacao_id, nome, quantidade, unidade_medida, data_vencimento, categoria_id)
    VALUES (%s, %s, %s, %s, %s, %s)
    RETURNING id;
"""
QUERY_INSERT_ALIMENTO_AVARIADO = """
    INSERT INTO alimentos_avariados (alimento_id, quantidade, descricao)
    VALUES (%s, %s, %s);
"""

# --- UPDATE (Usado pelo Agente Sanitário) ---
QUERY_APROVAR_DOACAO = """
    UPDATE doacoes_solicitadas
    SET status = 'APROVADA'
    WHERE id = %s
    RETURNING id;
"""
QUERY_REJEITAR_DOACAO = """
    UPDATE doacoes_solicitadas
    SET status = 'REJEITADA', observacao_vigilante = %s
    WHERE id = %s
    RETURNING id;
"""
QUERY_MOVER_ALIMENTOS_PARA_ESTOQUE ="""
    INSERT INTO alimentos(nome, categoria_id, quantidade, unidade_medida, data_vencimento)
    SELECT nome, categoria_id, quantidade, unidade_medida, data_vencimento
    FROM itens_solicitacao
    WHERE solicitacao_id = %s;
"""
