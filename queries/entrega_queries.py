# --- READ ---

QUERY_GET_ENTREGAS_PENDENTES = """
    SELECT 
        e.id, 
        e.cesta_id, 
        u.nome as recebedor_nome, 
        e.status,
        e.data_criacao
    FROM entregas e
    JOIN usuarios u ON e.recebedor_id = u.id
    WHERE e.status = 'PENDENTE'
    ORDER BY e.data_criacao ASC;
"""

QUERY_GET_ENTREGA_DETALHES = """
    SELECT
        e.id,
        e.cesta_id,
        r.nome as recebedor_nome,
        o.nome as operador_nome,
        e.status,
        e.data_criacao,
        e.data_entrega,
        e.observacao
    FROM entregas e
    JOIN usuarios r ON e.recebedor_id = r.id
    LEFT JOIN usuarios o ON e.operador_id = o.id
    WHERE e.id = %s;
"""

QUERY_GET_ALIMENTOS_CESTA = """
    SELECT
        a.nome,
        ac.quantidade_retirada
    FROM alimentos_cesta ac
    JOIN alimentos a ON ac.alimento_id = a.id
    WHERE ac.cesta_id = %s;
"""

# --- UPDATE ---

QUERY_CONFIRMAR_ENTREGA = """
    UPDATE entregas
    SET
        status = 'ENTREGUE',
        data_entrega = CURRENT_TIMESTAMP,
        operador_id = %s
    WHERE id = %s AND status = 'PENDENTE'
    RETURNING id;
"""

QUERY_CANCELAR_ENTREGA = """
    UPDATE entregas
    SET
        status = 'CANCELADA',
        observacao = %s
    WHERE id = %s
    RETURNING id;
"""

# --- CREATE ---

QUERY_CREATE_ENTREGA = """
    INSERT INTO entregas (cesta_id, recebedor_id)
    VALUES (%s, %s)
    RETURNING id;
"""
