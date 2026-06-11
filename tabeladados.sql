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

INSERT INTO usuarios(nome, username, senha, categoria) VALUES
('Pedro', 'pedro456', '123pedro', 'administrador'),
('Marcos', 'marco0', '12345678', 'Doador'),
('Paulo', 'paulo777', 'p4ul0', 'Nutricionista'),
('Lar Santa Luzia', 'larsl', '12345678', 'Recebedor');

INSERT INTO categorias(nome, refrigerado) VALUES
('Congelados', TRUE),
('Bebidas', TRUE),
('Temperos', FALSE);

INSERT INTO alimentos(nome, categoria_id, quantidade, unidade_medida, data_vencimento) VALUES
('Bandeja de coxa', 1, 7, 'UN', '2026-06-10'),
('Suco', 2, 10, 'L', '2026-06-15'),
('Sal', 3, 30, 'Kg', '2026-10-20');

INSERT INTO alimentos_avariados(alimento_id, quantidade, descricao) VALUES
(1, 3, 'PACOTE ABERTO'),
(2, 3, 'TÁ COM MUITO AÇUCAR'),
(3, 5, 'PACOTE COM QUANTIDADE ABAIXO DO PESO');

INSERT INTO doacoes_solicitadas (doador_id, data_solicitacao, status, observacao_vigilante) VALUES
(6, '2026-05-27', 'CONCLUIDO', 'Entregue e registrado no estoque central.'),
(3, '2026-06-04', 'APROVADO', 'Alimentos secos em perfeito estado.'),
(12, '2026-05-30', 'PENDENTE', 'Inspecionar integridade das embalagens na entrega.'),
(7, '2026-06-08', 'APROVADO', 'Alimentos secos em perfeito estado.'),
(4, '2026-05-03', 'REJEITADO', 'Data de validade vencida no lote de laticínios.'),
(3, '2026-05-30', 'REJEITADO', 'Sinais de umidade excessiva nos sacos de grãos.'),
(11, '2026-06-06', 'CONCLUIDO', 'Distribuição agendada para amanhã.'),
(15, '2026-05-04', 'APROVADO', 'Alimentos secos em perfeito estado.'),
(5, '2026-06-05', 'REJEITADO', 'Sinais de umidade excessiva nos sacos de grãos.'),
(13, '2026-05-24', 'APROVADO', 'Lote de vegetais limpo e higienizado.'),
(13, '2026-06-05', 'CONCLUIDO', 'Distribuição agendada para amanhã.'),
(15, '2026-05-16', 'CONCLUIDO', 'Armazenado na câmara fria 2.'),
(1, '2026-05-23', 'PENDENTE', 'Aguardando chegada do caminhão.'),
(1, '2026-06-05', 'APROVADO', 'Validade checada: tudo acima de 3 meses.'),
(5, '2026-05-16', 'APROVADO', 'Alimentos secos em perfeito estado.'),
(7, '2026-05-20', 'CONCLUIDO', 'Armazenado na câmara fria 2.'),
(6, '2026-05-25', 'REJEITADO', 'Produtos com embalagem violada.'),
(15, '2026-06-08', 'APROVADO', 'Validade checada: tudo acima de 3 meses.'),
(13, '2026-05-17', 'PENDENTE', NULL),
(15, '2026-05-20', 'APROVADO', 'Alimentos secos em perfeito estado.'),
(1, '2026-06-02', 'APROVADO', 'Lote de vegetais limpo e higienizado.'),
(9, '2026-05-11', 'APROVADO', 'Alimentos secos em perfeito estado.'),
(6, '2026-06-09', 'CONCLUIDO', 'Armazenado na câmara fria 2.'),
(10, '2026-05-22', 'PENDENTE', NULL),
(13, '2026-05-01', 'CONCLUIDO', 'Armazenado na câmara fria 2.'),
(5, '2026-05-03', 'PENDENTE', NULL),
(6, '2026-05-09', 'APROVADO', 'Validade checada: tudo acima de 3 meses.'),
(15, '2026-05-02', 'CONCLUIDO', 'Entregue e registrado no estoque central.'),
(2, '2026-05-27', 'PENDENTE', NULL),
(11, '2026-05-13', 'APROVADO', 'Alimentos secos em perfeito estado.'),
(6, '2026-05-10', 'CONCLUIDO', 'Armazenado na câmara fria 2.'),
(8, '2026-05-29', 'CONCLUIDO', 'Entregue e registrado no estoque central.'),
(13, '2026-05-11', 'CONCLUIDO', 'Armazenado na câmara fria 2.'),
(8, '2026-05-26', 'PENDENTE', NULL),
(3, '2026-05-04', 'APROVADO', 'Alimentos secos em perfeito estado.'),
(3, '2026-05-17', 'APROVADO', 'Validade checada: tudo acima de 3 meses.'),
(12, '2026-05-02', 'APROVADO', 'Alimentos secos em perfeito estado.'),
(4, '2026-05-12', 'APROVADO', 'Lote de vegetais limpo e higienizado.'),
(13, '2026-06-10', 'APROVADO', 'Lote de vegetais limpo e higienizado.'),
(3, '2026-05-18', 'PENDENTE', NULL),
(9, '2026-05-05', 'CONCLUIDO', 'Entregue e registrado no estoque central.'),
(13, '2026-05-01', 'PENDENTE', 'Aguardando chegada do caminhão.'),
(13, '2026-05-18', 'APROVADO', 'Lote de vegetais limpo e higienizado.'),
(15, '2026-05-06', 'PENDENTE', 'Inspecionar integridade das embalagens na entrega.'),
(1, '2026-05-20', 'PENDENTE', 'Inspecionar integridade das embalagens na entrega.'),
(5, '2026-05-02', 'APROVADO', 'Alimentos secos em perfeito estado.'),
(2, '2026-06-07', 'PENDENTE', 'Aguardando chegada do caminhão.'),
(6, '2026-05-29', 'PENDENTE', 'Aguardando chegada do caminhão.'),
(2, '2026-05-29', 'REJEITADO', 'Data de validade vencida no lote de laticínios.'),
(10, '2026-06-02', 'REJEITADO', 'Sinais de umidade excessiva nos sacos de grãos.');
