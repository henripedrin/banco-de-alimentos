QUERY_INSERT_RELATORIO = """
    INSERT INTO relatorios (file_name, reference_month, file_path)
    VALUES (%s, %s, %s)
    RETURNING id;
"""

QUERY_GET_ALL_RELATORIOS = "SELECT * FROM relatorios ORDER BY reference_month DESC;"

# Queries para buscar os dados para o relatório
# (Estes serão parametrizados com as datas de início e fim do mês)

QUERY_RELATORIO_DOACOES = """
    SELECT 
        COUNT(*) as total,
        SUM(CASE WHEN status = 'APROVADA' THEN 1 ELSE 0 END) as aprovadas,
        SUM(CASE WHEN status = 'REJEITADA' THEN 1 ELSE 0 END) as rejeitadas
    FROM doacoes_solicitadas
    WHERE data_solicitacao::date BETWEEN %s AND %s;
"""

QUERY_RELATORIO_TOP_DOADORES = """
    SELECT u.nome, COUNT(ds.id) as total_doacoes
    FROM doacoes_solicitadas ds
    JOIN usuarios u ON ds.doador_id = u.id
    WHERE ds.data_solicitacao::date BETWEEN %s AND %s
    GROUP BY u.nome
    ORDER BY total_doacoes DESC
    LIMIT 5;
"""

QUERY_RELATORIO_CESTAS = """
    SELECT 
        COUNT(*) as total_criadas
    FROM cestas_basicas
    WHERE data_montagem::date BETWEEN %s AND %s;
"""

QUERY_RELATORIO_ENTREGAS = """
    SELECT
        COUNT(*) as total,
        SUM(CASE WHEN status = 'ENTREGUE' THEN 1 ELSE 0 END) as entregues
    FROM entregas
    WHERE data_criacao::date BETWEEN %s AND %s;
"""

QUERY_RELATORIO_ALIMENTOS_DISTRIBUIDOS = """
    SELECT SUM(quantidade_retirada) as total
    FROM alimentos_cesta ac
    JOIN cestas_basicas cb ON ac.cesta_id = cb.id
    WHERE cb.data_montagem::date BETWEEN %s AND %s;
"""

QUERY_RELATORIO_ALIMENTOS_RECEBIDOS = """
    SELECT SUM(its.quantidade) as total
    FROM itens_solicitacao its
    JOIN doacoes_solicitadas ds ON its.solicitacao_id = ds.id
    WHERE ds.status = 'APROVADA' AND ds.data_solicitacao::date BETWEEN %s AND %s;
"""
