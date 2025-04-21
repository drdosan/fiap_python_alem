-- Tabela de robôs com ID autoincremento
CREATE TABLE robos (
    id_robo NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    modelo VARCHAR2(50),
    status VARCHAR2(20),
    ultima_localizacao VARCHAR2(100)
);

-- Tabela de colheita com chave estrangeira
CREATE TABLE soja_colheita (
    id_colheita NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_robo NUMBER,
    latitude NUMBER(10,6),
    longitude NUMBER(10,6),
    maturidade NUMBER(3),
    status VARCHAR2(20),
    data_coleta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_robo FOREIGN KEY (id_robo) REFERENCES robos(id_robo)
);