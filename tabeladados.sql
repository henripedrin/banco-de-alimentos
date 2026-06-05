DROP TABLE IF EXISTS usuarios;

CREATE TABLE usuarios(
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    username VARCHAR(50) NOT NULL,
    senha VARCHAR(30) NOT NULL,
    categoria VARCHAR(30) NOT NULL,
    ativo BOOLEAN DEFAULT TRUE
);

INSERT INTO usuarios(name,username, senha, categoria) VALUES
('Pedro', 'pedro456', '123pedro', 'administrador');