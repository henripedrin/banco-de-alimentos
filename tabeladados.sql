DROP TABLE IF EXISTS usuarios;

CREATE TABLE usuarios(
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    username VARCHAR(50) NOT NULL,
    senha VARCHAR(30) NOT NULL,
    categoria VARCHAR(30) NOT NULL,
    ativo BOOLEAN DEFAULT TRUE
);

CREATE TABLE categorias (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    refrigerado BOOLEAN DEFAULT FALSE
);

CREATE TABLE alimentos(
  id SERIAL PRIMARY KEY,
  name VARCHAR,
  categoria_id INT NOT NULL,
  quantidade INT,
  unidade VARCHAR(10),
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

INSERT INTO usuarios(name, username, senha, categoria) VALUES
('Pedro', 'pedro456', '123pedro', 'administrador'),
('Marcos', 'marco0', '12345678', 'Doador'),
('Paulo', 'paulo777', 'p4ul0', 'Nutricionista'),
('Lar Santa Luzia', 'larsl', '12345678', 'Recebedor');

INSERT INTO categorias(name, refrigerado) VALUES
('Congelados', TRUE),
('Bebidas', TRUE),
('Temperos', FALSE);

INSERT INTO alimentos( name, categoria_id, quantidade, unidade, data_vencimento) VALUES
('Bandeja de coxa', 1, 7, 'UN', '2026-06-10'),
('Suco', 2, 10, 'L', '2026-06-15'),
('Sal', 3, 30, 'Kg', '2026-10-20');

INSERT INTO alimentos_avariados(alimento_id, quantidade, descricao) VALUES
(1, 3, 'PACOTE ABERTO'),
(2, 3, 'TÁ COM MUITO AÇUCAR'),
(3, 5, 'PACOTE COM QUANTIDADE ABAIXO DO PESO')
