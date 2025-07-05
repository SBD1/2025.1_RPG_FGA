
-- --------------------------------------------------------------------------------------
-- Data Criacao ...........: 31/05/2025                                                --
-- Autor(es) ..............: Milena Marques                                            --
-- Versao ..............: 1.0                                                          --
-- Banco de Dados .........: PostgreSQL                                                --
-- Descricao .........: Inclusão de CREATE TABLE de todas as tabelas do banco de dados.--
-- --------------------------------------------------------------------------------------
-- | Atualizacao : 31/05/2025 | Autor(es): Milena Marques                       |      --
--                            | Descricao: Inclusão das linhas de CREATE TABLE  |      --
-- | Atualizacao : 04/07/2025 | Autor(es): Isaque Camargos e Ludmila Nunes      |      --
--                            | Descricao: Correção das linhas de CREATE TABLE  |      --
-- --------------------------------------------------------------------------------------

-- TABELAS BASE


CREATE TABLE tema (
    id_tema INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome CHAR(100) NOT NULL CHECK(nome IN ('Matemática', 'Programação', 'Engenharias', 'Gerais', 'Humanidades'))
);


CREATE TABLE tipoHabilidade (
    id_habilidade INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    tipo_habilidade CHAR(10) NOT NULL CHECK(tipo_habilidade IN ('ataque', 'cura', 'defesa'))
    
);


CREATE TABLE tipo_criatura (
    id_criatura INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    tipo_criatura CHAR(10) NOT NULL CHECK(tipo_criatura IN ('Monstro', 'Boss'))
    
);

-- lud alterou
CREATE TABLE campus (
    id_campus INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome CHAR(100) NOT NULL,
    descricao CHAR(255) NOT NULL
);


CREATE TABLE setor (
    id_setor INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_campus INT NOT NULL,
    nome CHAR(100) NOT NULL,
    descricao CHAR(255) NOT NULL,
    id_proxSetor INT,
    id_prevSetor INT,
    CONSTRAINT fk_id_campus FOREIGN KEY (id_campus) REFERENCES campus(id_campus),
    CONSTRAINT fk_id_proxSetor FOREIGN KEY (id_proxSetor) REFERENCES setor(id_setor),
    CONSTRAINT fk_id_prevSetor FOREIGN KEY (id_prevSetor) REFERENCES setor(id_setor)
);


CREATE TABLE sala_comum (
    id_sala INT GENERATED ALWAYS AS IDENTITY,
    id_setor INT NOT NULL,
    id_prevSala INT,
    id_proxSala INT,
    descricao CHAR(255) NOT NULL,
    nome CHAR(100) NOT NULL,
    tem_loja BOOLEAN NOT NULL,
    tem_dungeon BOOLEAN NOT NULL,
    UNIQUE (id_sala),
    PRIMARY KEY (id_sala, id_setor),
    CONSTRAINT fk_id_setor FOREIGN KEY (id_setor) REFERENCES setor(id_setor),
    CONSTRAINT fk_id_prevSala FOREIGN KEY (id_prevSala) REFERENCES sala_comum(id_sala),
    CONSTRAINT fk_id_proxSala FOREIGN KEY (id_proxSala) REFERENCES sala_comum(id_sala)
);


CREATE TABLE estudante (
    id_estudante INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome CHAR(100) NOT NULL,
    vida INT NOT NULL,
    estresse INT NOT NULL,
    total_dinheiro INT NOT NULL,
    id_sala INT NOT NULL,
    CONSTRAINT fk_id_sala FOREIGN KEY (id_sala) REFERENCES sala_comum(id_sala)
);


CREATE TABLE afinidade (
    id_estudante INT NOT NULL,
    id_tema INT NOT NULL,
    xp_atual INT NOT NULL,
    nivel_atual INT NOT NULL,
    PRIMARY KEY (id_estudante, id_tema),
    CONSTRAINT fk_estudante FOREIGN KEY (id_estudante) REFERENCES estudante(id_estudante),
    CONSTRAINT fk_tema FOREIGN KEY (id_tema) REFERENCES tema(id_tema)
);


CREATE TABLE dungeon_academica (
    id_dungeon INT NOT NULL PRIMARY KEY,
    nome CHAR(100) NOT NULL,
    descricao CHAR(255) NOT NULL,
    id_tema INT NOT NULL,
    CONSTRAINT fk_id_dungeon FOREIGN KEY (id_dungeon) REFERENCES sala_comum(id_sala),
    CONSTRAINT fk_id_tema FOREIGN KEY (id_tema) REFERENCES tema(id_tema)
);

CREATE TABLE tipo_item (
    id_item INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    item_tipo CHAR(10) CHECK (item_tipo IN ('Consumível', 'Equipável', 'Monetário', 'Relíquia'))
);

CREATE TABLE reliquia (
    id_reliquia INT NOT NULL PRIMARY KEY,
    nome CHAR(100) NOT NULL,
    descricao CHAR(255) NOT NULL,
    tipo_reliquia CHAR(100) NOT NULL,
    CONSTRAINT fk_id_reliquia FOREIGN KEY (id_reliquia) REFERENCES tipo_item(id_item)
);

-- isaque já alterou
CREATE TABLE boss (
    id_criatura INT NOT NULL PRIMARY KEY,
    id_reliquia INT NOT NULL,
    nome CHAR(100) NOT NULL,
    descricao CHAR(255) NOT NULL,
    nivel INT NOT NULL,
    vida_max INT NOT NULL,
    
    CONSTRAINT fk_id_criatura FOREIGN KEY (id_criatura) REFERENCES tipo_criatura(id_criatura),
    CONSTRAINT fk_reliquia FOREIGN KEY (id_reliquia) REFERENCES reliquia(id_reliquia)
);


-- isaque já alterou
CREATE TABLE monstro_simples (
    id_criatura INT NOT NULL PRIMARY KEY,
    nome CHAR(100) NOT NULL,
    descricao CHAR(255) NOT NULL,
    nivel INT NOT NULL,
    vida_max INT NOT NULL,
    xp_tema INT NOT NULL,
    qtd_moedas INT NOT NULL CHECK (qtd_moedas >= 0),

    CONSTRAINT fk_id_criatura FOREIGN KEY (id_criatura) REFERENCES tipo_criatura(id_criatura)
);


CREATE TABLE instancia_de_criatura (
    id_instanciaCriatura INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_criatura INT NOT NULL,
    vida_atual INT NOT NULL,
    id_dungeon INT NOT NULL,
    CONSTRAINT fk_criatura FOREIGN KEY (id_criatura) REFERENCES tipo_criatura(id_criatura),
    CONSTRAINT fk_dungeon FOREIGN KEY (id_dungeon) REFERENCES dungeon_academica(id_dungeon)
);


CREATE TABLE consumivel (
    id_item INT NOT NULL PRIMARY KEY,
    nome CHAR(100) NOT NULL,
    descricao CHAR(255) NOT NULL,
    efeito FLOAT NOT NULL,
    preco FLOAT NOT NULL,
    CONSTRAINT fk_id_item FOREIGN KEY (id_item) REFERENCES tipo_item(id_item)
);


CREATE TABLE equipavel (
    id_item INT NOT NULL PRIMARY KEY,
    nome CHAR(100) NOT NULL,
    descricao CHAR(255) NOT NULL,
    efeito INT NOT NULL,
    preco INT NOT NULL,
    equipado BOOLEAN NOT NULL,
    CONSTRAINT fk_id_item FOREIGN KEY (id_item) REFERENCES tipo_item(id_item)
);


CREATE TABLE monetario (
    id_item INT NOT NULL PRIMARY KEY,
    nome CHAR(100) NOT NULL,
    descricao CHAR(255) NOT NULL,
    valor INT NOT NULL,
    CONSTRAINT fk_id_item FOREIGN KEY (id_item) REFERENCES tipo_item(id_item)
);


CREATE TABLE loja_item (
    id_sala INT NOT NULL,
    id_item INT NOT NULL,
    PRIMARY KEY (id_sala, id_item),
    CONSTRAINT fk_sala FOREIGN KEY (id_sala) REFERENCES sala_comum(id_sala),
    CONSTRAINT fk_item FOREIGN KEY (id_item) REFERENCES tipo_item(id_item)
);


CREATE TABLE habilidade_criatura (
    id_criatura INT NOT NULL,
    id_habilidade INT NOT NULL,
    PRIMARY KEY (id_criatura, id_habilidade),
    CONSTRAINT fk_criatura FOREIGN KEY (id_criatura) REFERENCES tipo_criatura(id_criatura),
    CONSTRAINT fk_habilidade FOREIGN KEY (id_habilidade) REFERENCES tipoHabilidade(id_habilidade)
);


CREATE TABLE habilidade_estudante (
    id_estudante INT NOT NULL,
    id_habilidade INT NOT NULL,
    PRIMARY KEY (id_estudante, id_habilidade),
    CONSTRAINT fk_estudante FOREIGN KEY (id_estudante) REFERENCES estudante(id_estudante),
    CONSTRAINT fk_habilidade FOREIGN KEY (id_habilidade) REFERENCES tipoHabilidade(id_habilidade)
);

-- CREATE TABLE loja (
--     id_loja INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
--     nome CHAR(100) NOT NULL
-- );

CREATE TABLE habilidade_loja (
    id_loja INT NOT NULL,
    id_habilidade INT NOT NULL,
    PRIMARY KEY (id_loja, id_habilidade),
    CONSTRAINT fk_loja FOREIGN KEY (id_loja) REFERENCES sala_comum(id_sala),
    CONSTRAINT fk_habilidade FOREIGN KEY (id_habilidade) REFERENCES tipoHabilidade(id_habilidade)
);


CREATE TABLE instancia_de_item (
    id_instanciaItem INT GENERATED ALWAYS AS IDENTITY,
    id_item INT NOT NULL,
    id_sala INT,
    id_estudante INT,
    PRIMARY KEY (id_instanciaItem, id_item),
    CONSTRAINT fk_id_item FOREIGN KEY (id_item) REFERENCES tipo_item(id_item),
    CONSTRAINT fk_id_sala FOREIGN KEY (id_sala) REFERENCES sala_comum(id_sala),
    CONSTRAINT fk_id_estudante FOREIGN KEY (id_estudante) REFERENCES estudante(id_estudante)
);


CREATE TABLE Ataque (
    id_habilidade INT NOT NULL PRIMARY KEY,
    id_tema INT NOT NULL,
    nome CHAR(100) NOT NULL,
    nivel INT NOT NULL,
    coolDown INT NOT NULL,
    danoCausado INT NOT NULL,
    CONSTRAINT fk_habilidade FOREIGN KEY (id_habilidade) REFERENCES tipoHabilidade(id_habilidade),
    CONSTRAINT fk_id_tema FOREIGN KEY (id_tema) REFERENCES tema(id_tema)
);


CREATE TABLE Cura (
    id_habilidade INT NOT NULL PRIMARY KEY,
    id_tema INT NOT NULL,
    nome CHAR(100) NOT NULL,
    nivel INT NOT NULL,
    coolDown INT NOT NULL,
    vidaRecuperada INT NOT NULL,
    CONSTRAINT fk_id_habilidade FOREIGN KEY (id_habilidade) REFERENCES tipoHabilidade(id_habilidade),
    CONSTRAINT fk_id_tema FOREIGN KEY (id_tema) REFERENCES tema(id_tema)
);


CREATE TABLE Defesa (
    id_habilidade INT NOT NULL PRIMARY KEY,
    id_tema INT NOT NULL,
    nome CHAR(100) NOT NULL,
    nivel INT NOT NULL,
    coolDown INT NOT NULL,
    danoMitigado INT NOT NULL,
    CONSTRAINT fk_id_habilidade FOREIGN KEY (id_habilidade) REFERENCES tipoHabilidade(id_habilidade),
    CONSTRAINT fk_id_tema FOREIGN KEY (id_tema) REFERENCES tema(id_tema)
);