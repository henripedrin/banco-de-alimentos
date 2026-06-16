# Queries para buscar dados agregados para os dashboards

# --- Admin Dashboard ---
QUERY_COUNT_USERS_BY_CATEGORY = """
    SELECT categoria, COUNT(*) as total
    FROM usuarios
    GROUP BY categoria;
"""
QUERY_COUNT_ALIMENTOS = "SELECT COUNT(*) as total FROM alimentos;"
QUERY_COUNT_DOACOES = "SELECT COUNT(*) as total FROM doacoes_solicitadas;"
QUERY_COUNT_CESTAS = "SELECT COUNT(*) as total FROM cestas_basicas;"
QUERY_RECENT_ACTIVITIES = """
    SELECT 'Nova Cesta' as acao, 'Cesta montada por ID: ' || nutricionista_id as detalhe, data_montagem as data
    FROM cestas_basicas
    UNION ALL
    SELECT 'Nova Doação' as acao, 'Doação ID: ' || id as detalhe, data_solicitacao as data
    FROM doacoes_solicitadas
    ORDER BY data DESC
    LIMIT 5;
"""
