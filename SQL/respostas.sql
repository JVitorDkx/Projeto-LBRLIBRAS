CREATE TABLE respostas (
    id SERIAL PRIMARY KEY,
    usuario_id UUID REFERENCES usuarios(id),
    questao_id INT REFERENCES questoes(id),
    resposta TEXT NOT NULL,
    correta BOOLEAN NOT NULL
);
