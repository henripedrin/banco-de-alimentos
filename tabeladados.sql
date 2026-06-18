DROP TABLE IF EXISTS alimentos CASCADE;
DROP TABLE IF EXISTS alimentos_avariados CASCADE;
DROP TABLE IF EXISTS categorias CASCADE;
DROP TABLE IF EXISTS doacoes_solicitadas CASCADE;
DROP TABLE IF EXISTS itens_solicitacao CASCADE;
DROP TABLE IF EXISTS usuarios CASCADE;
DROP TABLE IF EXISTS cestas_basicas CASCADE;
DROP TABLE IF EXISTS alimentos_cesta CASCADE;
DROP TABLE IF EXISTS entregas CASCADE;


CREATE TABLE usuarios(
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    username VARCHAR(50) NOT NULL,
    senha VARCHAR(255) NOT NULL, -- Aumentado para armazenar hashes
    categoria VARCHAR(30) NOT NULL,
    ativo BOOLEAN DEFAULT TRUE,
    data_cadastro TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
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
  CONSTRAINT fk_alimento_categoria FOREIGN KEY (categoria_id) REFERENCES categorias(id)
);

CREATE TABLE doacoes_solicitadas (
    id SERIAL PRIMARY KEY,
    doador_id INT NOT NULL,
    data_solicitacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'PENDENTE',
    observacao_vigilante TEXT,
    CONSTRAINT fk_doacao_doador FOREIGN KEY (doador_id) REFERENCES usuarios(id)
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

CREATE TABLE alimentos_avariados (
    id SERIAL PRIMARY KEY,
    item_solicitacao_id INT NOT NULL, -- Chave estrangeira para o item doado
    quantidade INT NOT NULL,
    descricao TEXT NOT NULL,
    data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_avaria_item_solicitacao FOREIGN KEY (item_solicitacao_id) REFERENCES itens_solicitacao(id) ON DELETE CASCADE
);

CREATE TABLE cestas_basicas (
    id SERIAL PRIMARY KEY,
    nutricionista_id INT NOT NULL,
    data_montagem TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    recebedor_id INT NOT NULL,
    CONSTRAINT fk_cesta_nutricionista FOREIGN KEY (nutricionista_id) REFERENCES usuarios(id),
    CONSTRAINT fk_cesta_recebedor FOREIGN KEY (recebedor_id) REFERENCES usuarios(id)
);

CREATE TABLE alimentos_cesta (
    id SERIAL PRIMARY KEY,
    cesta_id INT NOT NULL,
    alimento_id INT NOT NULL,
    quantidade_retirada INT NOT NULL,
    CONSTRAINT fk_ac_cesta FOREIGN KEY (cesta_id) REFERENCES cestas_basicas(id) ON DELETE CASCADE,
    CONSTRAINT fk_ac_alimento FOREIGN KEY (alimento_id) REFERENCES alimentos(id) ON DELETE CASCADE
);

CREATE TABLE entregas (
    id SERIAL PRIMARY KEY,
    cesta_id INT NOT NULL,
    recebedor_id INT NOT NULL,
    operador_id INT,
    status VARCHAR(20) DEFAULT 'PENDENTE',
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    data_entrega TIMESTAMP,
    observacao TEXT,
    CONSTRAINT fk_entrega_cesta FOREIGN KEY (cesta_id) REFERENCES cestas_basicas(id),
    CONSTRAINT fk_entrega_recebedor FOREIGN KEY (recebedor_id) REFERENCES usuarios(id),
    CONSTRAINT fk_entrega_operador FOREIGN KEY (operador_id) REFERENCES usuarios(id)
);

-- =====================================
-- USUÁRIOS
-- =====================================
-- Senhas em texto plano para facilitar testes iniciais. Em produção, usar hashes.
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
('Grãos', FALSE), ('Massas', FALSE), ('Enlatados', FALSE),
('Laticínios', TRUE), ('Carnes', TRUE), ('Hortifruti', TRUE),
('Bebidas', TRUE), ('Padaria', FALSE), ('Higiene', FALSE), ('Limpeza', FALSE);

-- =====================================
-- ALIMENTOS (ESTOQUE INICIAL)
-- =====================================
INSERT INTO alimentos (nome, categoria_id, quantidade, unidade_medida, data_vencimento) VALUES
('Arroz Agulhinha', 1, 500, 'kg', '2027-01-15'),
('Feijão Carioca', 1, 350, 'kg', '2026-12-10'),
('Macarrão Espaguete', 2, 400, 'pct', '2027-03-20'),
('Leite Integral UHT', 4, 250, 'L', '2026-07-15'),
('Queijo Mussarela', 4, 80, 'kg', '2026-07-01'),
('Frango Congelado', 5, 150, 'kg', '2026-08-10'),
('Carne Bovina Moída', 5, 100, 'kg', '2026-08-05'),
('Batata Inglesa', 6, 300, 'kg', '2026-06-25'),
('Cenoura', 6, 200, 'kg', '2026-06-28'),
('Suco de Uva Integral', 7, 180, 'L', '2027-02-12'),
('Pão Integral', 8, 120, 'pct', '2026-06-15');

-- =====================================
-- DOAÇÕES SOLICITADAS
-- =====================================
INSERT INTO doacoes_solicitadas (doador_id, status, observacao_vigilante) VALUES
(7, 'APROVADA', 'Alimentos em boas condições, sem avarias.'),
(8, 'PENDENTE', NULL),
(9, 'REJEITADA', 'Produtos vencidos encontrados na amostra.'),
(7, 'PENDENTE', NULL);

-- =====================================
-- ITENS DAS SOLICITAÇÕES
-- =====================================
INSERT INTO itens_solicitacao (solicitacao_id, nome, quantidade, unidade_medida, data_vencimento, categoria_id) VALUES
(1, 'Arroz Parboilizado', 100, 'kg', '2027-01-15', 1),
(1, 'Feijão Preto', 80, 'kg', '2026-12-10', 1),
(2, 'Macarrão Parafuso', 150, 'pct', '2027-03-20', 2),
(2, 'Leite Desnatado', 100, 'L', '2026-07-15', 4),
(3, 'Carne Bovina (Patinho)', 50, 'kg', '2025-01-01', 5),
(4, 'Sabonete', 200, 'un', '2029-01-01', 9),
(4, 'Creme Dental', 150, 'un', '2028-06-01', 9);

-- =====================================
-- CESTAS BÁSICAS
-- =====================================
INSERT INTO cestas_basicas (nutricionista_id, recebedor_id) VALUES
(2, 5), (2, 6);

-- =====================================
-- ALIMENTOS DAS CESTAS
-- =====================================
INSERT INTO alimentos_cesta (cesta_id, alimento_id, quantidade_retirada) VALUES
(1, 1, 10), (1, 2, 10), (1, 3, 8), (1, 4, 5),
(2, 1, 12), (2, 2, 12), (2, 3, 10), (2, 11, 6);

-- =====================================
-- ENTREGAS
-- =====================================
INSERT INTO entregas (cesta_id, recebedor_id, operador_id, status, data_entrega, observacao) VALUES
(1, 5, 4, 'ENTREGUE', (CURRENT_TIMESTAMP - interval '2 days'), 'Entrega realizada no período da manhã.'),
(2, 6, NULL, 'PENDENTE', NULL, NULL);

-- =====================================
-- COMPLEMENTO DE DADOS (NOVO)
-- =====================================
INSERT INTO usuarios (nome, username, senha, categoria, ativo) VALUES
('Ana Nutri', 'nutri02', '123456', 'NUTRICIONISTA', true),
('Marcos Agente', 'sanitario02', '123456', 'AGENTE_SANITARIO', true),
('Lucas Log', 'logistica02', '123456', 'OPERADOR_LOGISTICO', true),
('ONG Amigo Fiel', 'recebedor03', '123456', 'RECEBEDOR', true),
('Restaurante Sabor Divino', 'doador04', '123456', 'DOADOR', true),
('Usuário Inativo', 'inativo01', '123456', 'DOADOR', false);

INSERT INTO alimentos (nome, categoria_id, quantidade, unidade_medida, data_vencimento) VALUES
('Farinha de Trigo', 2, 200, 'kg', '2028-05-20'),
('Óleo de Soja', 3, 300, 'L', '2027-11-30'),
('Sardinha em Lata', 3, 400, 'un', '2029-01-01'),
('Iogurte Natural', 4, 150, 'un', (current_date + interval '1 day')),
('Maçã', 6, 250, 'kg', (current_date + interval '5 days')),
('Tomate', 6, 180, 'kg', (current_date - interval '2 days')),
('Biscoito Cream Cracker', 8, 500, 'pct', '2027-08-08'),
('Detergente', 10, 100, 'L', '2030-01-01');

INSERT INTO doacoes_solicitadas (doador_id, status, observacao_vigilante) VALUES
(15, 'PENDENTE', NULL);

INSERT INTO itens_solicitacao (solicitacao_id, nome, quantidade, unidade_medida, data_vencimento, categoria_id) VALUES
(5, 'Farinha de Trigo', 50, 'kg', '2028-05-20', 2),
(5, 'Óleo de Soja', 30, 'L', '2027-11-30', 3);

INSERT INTO cestas_basicas (nutricionista_id, recebedor_id) VALUES
(10, 13);

INSERT INTO alimentos_cesta (cesta_id, alimento_id, quantidade_retirada) VALUES
(3, 12, 20), (3, 13, 10), (3, 14, 24);

INSERT INTO entregas (cesta_id, recebedor_id, status) VALUES
(3, 13, 'PENDENTE');

-- =====================================
-- AJUSTE DOS SEQUENCES
-- =====================================
SELECT setval('usuarios_id_seq', (SELECT MAX(id) FROM usuarios));
SELECT setval('categorias_id_seq', (SELECT MAX(id) FROM categorias));
SELECT setval('alimentos_id_seq', (SELECT MAX(id) FROM alimentos));
SELECT setval('alimentos_avariados_id_seq', (SELECT MAX(id) FROM alimentos_avariados), false);
SELECT setval('doacoes_solicitadas_id_seq', (SELECT MAX(id) FROM doacoes_solicitadas));
SELECT setval('itens_solicitacao_id_seq', (SELECT MAX(id) FROM itens_solicitacao));
SELECT setval('cestas_basicas_id_seq', (SELECT MAX(id) FROM cestas_basicas));
SELECT setval('alimentos_cesta_id_seq', (SELECT MAX(id) FROM alimentos_cesta));
SELECT setval('entregas_id_seq', (SELECT MAX(id) FROM entregas));
