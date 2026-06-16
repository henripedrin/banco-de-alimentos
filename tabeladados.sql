DROP TABLE IF EXISTS alimentos;
DROP TABLE IF EXISTS alimentos_avariados;
DROP TABLE IF EXISTS categorias CASCADE;
DROP TABLE IF EXISTS doacoes_solicitadas CASCADE ;
DROP TABLE IF EXISTS itens_solicitacao;
DROP TABLE IF EXISTS usuarios;
DROP TABLE IF EXISTS cestas_basicas;
DROP TABLE IF EXISTS alimentos_cesta;


CREATE TABLE usuarios(
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    username VARCHAR(50) NOT NULL,
    senha VARCHAR(30) NOT NULL,
    categoria VARCHAR(30) NOT NULL,
    ativo BOOLEAN DEFAULT TRUE
);

CREATE TABLE categorias (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) UNIQUE NOT NULL,
    refrigerado BOOLEAN DEFAULT FALSE
);

CREATE TABLE alimentos(
  id SERIAL PRIMARY KEY,
  nome VARCHAR,
  categoria_id INT NOT NULL,
  quantidade INT,
  unidade_medida VARCHAR(10),
  data_vencimento DATE NOT NULL,
  CONSTRAINT fk_avaria_alimento FOREIGN KEY (id) REFERENCES alimentos(id) ON DELETE CASCADE
);

CREATE TABLE alimentos_avariados (
    id SERIAL PRIMARY KEY,
    alimento_id INT NOT NULL,
    quantidade INT NOT NULL,
    descricao TEXT NOT NULL,
    data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE doacoes_solicitadas (
    id SERIAL PRIMARY KEY,
    doador_id INT NOT NULL,
    data_solicitacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'PENDENTE',
    observacao_vigilante TEXT
);

CREATE TABLE itens_solicitacao (
    id SERIAL PRIMARY KEY,
    solicitacao_id INT NOT NULL,
    nome VARCHAR(100) NOT NULL,
    quantidade INT NOT NULL,
    unidade_medida VARCHAR(10) NOT NULL,
    data_vencimento DATE NOT NULL,
    categoria_id INT NOT NULL,

    CONSTRAINT fk_solicitacao FOREIGN KEY (solicitacao_id) REFERENCES doacoes_solicitadas(id) ON DELETE CASCADE,
    CONSTRAINT fk_categoria FOREIGN KEY (categoria_id) REFERENCES categorias(id)
);

CREATE TABLE cestas_basicas (
    id SERIAL PRIMARY KEY,
    nutricionista_id INT NOT NULL,
    data_montagem TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    recebedor_id INT NOT NULL
);

CREATE TABLE alimentos_cesta (
    id SERIAL PRIMARY KEY,
    cesta_id INT NOT NULL,
    alimento_id INT NOT NULL,
    quantidade_retirada INT NOT NULL
);
-- =====================================
-- USUÁRIOS
-- =====================================

INSERT INTO usuarios (nome, username, senha, categoria) VALUES
                                                            ('Administrador Geral', 'admin', '123456', 'ADMINISTRADOR'),
                                                            ('Maria Nutricionista', 'nutri01', '123456', 'NUTRICIONISTA'),
                                                            ('Carlos Sanitário', 'sanitario01', '123456', 'AGENTE_SANITARIO'),
                                                            ('Pedro Logística', 'logistica01', '123456', 'OPERADOR_LOGISTICO'),
                                                            ('Lar Esperança', 'recebedor01', '123456', 'RECEBEDOR'),
                                                            ('Casa do Bem', 'recebedor02', '123456', 'RECEBEDOR'),
                                                            ('João Silva', 'doador01', '123456', 'DOADOR'),
                                                            ('Mercado Central', 'doador02', '123456', 'DOADOR'),
                                                            ('Supermercado Econômico', 'doador03', '123456', 'DOADOR');

-- =====================================
-- CATEGORIAS
-- =====================================

INSERT INTO categorias (nome, refrigerado) VALUES
                                               ('Grãos', FALSE),
                                               ('Massas', FALSE),
                                               ('Enlatados', FALSE),
                                               ('Laticínios', TRUE),
                                               ('Carnes', TRUE),
                                               ('Hortifruti', TRUE),
                                               ('Bebidas', TRUE),
                                               ('Padaria', FALSE);

-- =====================================
-- ALIMENTOS
-- =====================================

INSERT INTO alimentos
(nome, categoria_id, quantidade, unidade_medida, data_vencimento)
VALUES
    ('Arroz', 1, 500, 'kg', '2027-01-15'),
    ('Feijão Carioca', 1, 350, 'kg', '2026-12-10'),
    ('Macarrão Espaguete', 2, 400, 'pct', '2027-03-20'),
    ('Leite Integral', 4, 250, 'L', '2026-07-15'),
    ('Queijo Mussarela', 4, 80, 'kg', '2026-07-01'),
    ('Frango Congelado', 5, 150, 'kg', '2026-08-10'),
    ('Carne Bovina', 5, 100, 'kg', '2026-08-05'),
    ('Batata', 6, 300, 'kg', '2026-06-25'),
    ('Cenoura', 6, 200, 'kg', '2026-06-28'),
    ('Suco de Uva', 7, 180, 'L', '2027-02-12'),
    ('Pão Integral', 8, 120, 'pct', '2026-06-15');

-- =====================================
-- ALIMENTOS AVARIADOS
-- =====================================

INSERT INTO alimentos_avariados
(alimento_id, quantidade, descricao)
VALUES
    (4, 10, 'Embalagens estouradas'),
    (8, 15, 'Batatas deterioradas'),
    (11, 5, 'Pacotes com mofo');

-- =====================================
-- SOLICITAÇÕES DE DOAÇÃO
-- =====================================

INSERT INTO doacoes_solicitadas
(doador_id, status, observacao_vigilante)
VALUES
    (7, 'APROVADA', 'Alimentos em boas condições'),
    (8, 'PENDENTE', NULL),
    (9, 'REJEITADA', 'Produtos vencidos encontrados');

-- =====================================
-- ITENS DAS SOLICITAÇÕES
-- =====================================

INSERT INTO itens_solicitacao
(solicitacao_id, nome, quantidade, unidade_medida, data_vencimento, categoria_id)
VALUES
    (1, 'Arroz', 100, 'kg', '2027-01-15', 1),
    (1, 'Feijão Carioca', 80, 'kg', '2026-12-10', 1),

    (2, 'Macarrão Espaguete', 150, 'pct', '2027-03-20', 2),
    (2, 'Leite Integral', 100, 'L', '2026-07-15', 4),

    (3, 'Carne Bovina', 50, 'kg', '2025-01-01', 5);

-- =====================================
-- CESTAS BÁSICAS
-- =====================================

INSERT INTO cestas_basicas
(nutricionista_id, recebedor_id)
VALUES
    (2, 5),
    (2, 6);

-- =====================================
-- ALIMENTOS DAS CESTAS
-- =====================================

INSERT INTO alimentos_cesta
(cesta_id, alimento_id, quantidade_retirada)
VALUES
-- Cesta 1
(1, 1, 10),
(1, 2, 10),
(1, 3, 8),
(1, 4, 5),

-- Cesta 2
(2, 1, 12),
(2, 2, 12),
(2, 3, 10),
(2, 10, 6);

-- =====================================
-- AJUSTE DOS SEQUENCES
-- =====================================

SELECT setval('usuarios_id_seq', (SELECT MAX(id) FROM usuarios));
SELECT setval('categorias_id_seq', (SELECT MAX(id) FROM categorias));
SELECT setval('alimentos_id_seq', (SELECT MAX(id) FROM alimentos));
SELECT setval('alimentos_avariados_id_seq', (SELECT MAX(id) FROM alimentos_avariados));
SELECT setval('doacoes_solicitadas_id_seq', (SELECT MAX(id) FROM doacoes_solicitadas));
SELECT setval('itens_solicitacao_id_seq', (SELECT MAX(id) FROM itens_solicitacao));
SELECT setval('cestas_basicas_id_seq', (SELECT MAX(id) FROM cestas_basicas));
SELECT setval('alimentos_cesta_id_seq', (SELECT MAX(id) FROM alimentos_cesta));