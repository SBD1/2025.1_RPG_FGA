
-- --------------------------------------------------------------------------------------
-- Data Criacao ...........: 31/05/2025                                                --
-- Autor(es) ..............: Milena Marques                                            --
-- Versao ..............: 2.0                                                          --
-- Banco de Dados .........: PostgreSQL                                                --
-- Descricao .........: Inclusão de CREATE TABLE de todas as tabelas do banco de dados.--
-- --------------------------------------------------------------------------------------
-- | Atualizacao : 31/05/2025 | Autor(es): Milena Marques                       |      --
--                            | Descricao: Inclusão das linhas de CREATE TABLE  |      --
-- | Atualizacao : 05/07/2025 | Autor(es): Isaque Camargos e Ludmila Nunes      |      --
--                            | Descricao: Correção das linhas de CREATE TABLE  |      --
-- --------------------------------------------------------------------------------------

-- TABELAS BASE
CREATE TABLE tipoHabilidade (
    id_habilidade INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    tipo_habilidade CHAR(10) NOT NULL CHECK(tipo_habilidade IN ('ataque', 'cura', 'defesa'))
    
);

CREATE TABLE tema (
    id_tema INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome CHAR(100) NOT NULL CHECK(nome IN ('Matemática', 'Programação', 'Engenharias', 'Gerais', 'Humanidades'))
);

CREATE TABLE Ataque (
    id_ataque_habilidade INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, -- Novo PK próprio
    id_tipo_habilidade INT NOT NULL, -- FK para tipoHabilidade
    id_tema INT NOT NULL,
    nome CHAR(100) NOT NULL,
    nivel INT NOT NULL,
    coolDown INT NOT NULL,
    danoCausado INT NOT NULL,
    CONSTRAINT fk_tipo_habilidade_ataque FOREIGN KEY (id_tipo_habilidade) REFERENCES tipoHabilidade(id_habilidade),
    CONSTRAINT fk_id_tema FOREIGN KEY (id_tema) REFERENCES tema(id_tema)
);

CREATE TABLE Cura (
    id_cura_habilidade INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, -- Novo PK próprio
    id_tipo_habilidade INT NOT NULL, -- FK para tipoHabilidade
    id_tema INT NOT NULL,
    nome CHAR(100) NOT NULL,
    nivel INT NOT NULL,
    coolDown INT NOT NULL,
    vidaRecuperada INT NOT NULL,
    CONSTRAINT fk_tipo_habilidade_cura FOREIGN KEY (id_tipo_habilidade) REFERENCES tipoHabilidade(id_habilidade),
    CONSTRAINT fk_id_tema FOREIGN KEY (id_tema) REFERENCES tema(id_tema)
);

CREATE TABLE Defesa (
    id_defesa_habilidade INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, -- Novo PK próprio
    id_tipo_habilidade INT NOT NULL, -- FK para tipoHabilidade
    id_tema INT NOT NULL,
    nome CHAR(100) NOT NULL,
    nivel INT NOT NULL,
    coolDown INT NOT NULL,
    danoMitigado INT NOT NULL,
    CONSTRAINT fk_tipo_habilidade_defesa FOREIGN KEY (id_tipo_habilidade) REFERENCES tipoHabilidade(id_habilidade),
    CONSTRAINT fk_id_tema FOREIGN KEY (id_tema) REFERENCES tema(id_tema)
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
    id_reliquia INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, 
    nome CHAR(100) NOT NULL,
    descricao CHAR(255) NOT NULL,
    tipo_reliquia CHAR(100) NOT NULL, 
    id_tipo_item INT NOT NULL, -- Nova FK para tipo_item
    CONSTRAINT fk_tipo_item_reliquia FOREIGN KEY (id_tipo_item) REFERENCES tipo_item(id_item)
);

-- DDL Corrigido para boss
CREATE TABLE boss (
    id_boss INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, -- ID único para cada boss
    id_tipo_criatura INT NOT NULL, -- FK para tipo_criatura
    id_reliquia INT NOT NULL,
    nome CHAR(100) NOT NULL,
    descricao CHAR(255) NOT NULL,
    nivel INT NOT NULL,
    vida_max INT NOT NULL,
    CONSTRAINT fk_tipo_criatura_boss FOREIGN KEY (id_tipo_criatura) REFERENCES tipo_criatura(id_criatura),
    CONSTRAINT fk_reliquia FOREIGN KEY (id_reliquia) REFERENCES reliquia(id_reliquia)
);

-- DDL Corrigido para monstro_simples
CREATE TABLE monstro_simples (
    id_monstro_simples INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, -- ID único para cada monstro simples
    id_tipo_criatura INT NOT NULL, -- FK para tipo_criatura
    nome CHAR(100) NOT NULL,
    descricao CHAR(255) NOT NULL,
    nivel INT NOT NULL,
    vida_max INT NOT NULL,
    xp_tema INT NOT NULL,
    qtd_moedas INT NOT NULL CHECK (qtd_moedas >= 0),
    CONSTRAINT fk_tipo_criatura_monstro FOREIGN KEY (id_tipo_criatura) REFERENCES tipo_criatura(id_criatura)
);

-- DDL Corrigido para instancia_de_criatura
CREATE TABLE instancia_de_criatura (
    id_instanciaCriatura INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_monstro_simples INT, -- Referencia monstro_simples
    id_boss INT, -- Referencia boss
    vida_atual INT NOT NULL,
    id_dungeon INT NOT NULL,
    CONSTRAINT fk_monstro_simples FOREIGN KEY (id_monstro_simples) REFERENCES monstro_simples(id_monstro_simples),
    CONSTRAINT fk_boss FOREIGN KEY (id_boss) REFERENCES boss(id_boss),
    CONSTRAINT fk_dungeon FOREIGN KEY (id_dungeon) REFERENCES dungeon_academica(id_dungeon),
    CONSTRAINT chk_criatura_type CHECK ( (id_monstro_simples IS NOT NULL AND id_boss IS NULL) OR (id_monstro_simples IS NULL AND id_boss IS NOT NULL) )
);

-- DDL Corrigido para consumivel
CREATE TABLE consumivel (
    id_consumivel INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, -- ID único para cada item consumível
    id_tipo_item INT NOT NULL, -- FK para tipo_item (tipo 'Consumível')
    nome CHAR(100) NOT NULL,
    descricao CHAR(255) NOT NULL,
    efeito FLOAT NOT NULL,
    preco FLOAT NOT NULL,
    CONSTRAINT fk_tipo_item_consumivel FOREIGN KEY (id_tipo_item) REFERENCES tipo_item(id_item)
);

-- DDL Corrigido para equipavel
CREATE TABLE equipavel (
    id_equipavel INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, -- ID único para cada item equipável
    id_tipo_item INT NOT NULL, -- FK para tipo_item (tipo 'Equipável')
    nome CHAR(100) NOT NULL,
    descricao CHAR(255) NOT NULL,
    efeito INT NOT NULL,
    preco INT NOT NULL,
    equipado BOOLEAN NOT NULL,
    CONSTRAINT fk_tipo_item_equipavel FOREIGN KEY (id_tipo_item) REFERENCES tipo_item(id_item)
);

-- DDL Corrigido para monetario
CREATE TABLE monetario (
    id_monetario INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, -- ID único para cada item monetário
    id_tipo_item INT NOT NULL, -- FK para tipo_item (tipo 'Monetário')
    nome CHAR(100) NOT NULL,
    descricao CHAR(255) NOT NULL,
    valor INT NOT NULL,
    CONSTRAINT fk_tipo_item_monetario FOREIGN KEY (id_tipo_item) REFERENCES tipo_item(id_item)
);

CREATE TABLE loja_item (
    id_sala INT NOT NULL,
    id_consumivel INT NOT NULL,
    PRIMARY KEY (id_sala, id_consumivel),
    CONSTRAINT fk_sala FOREIGN KEY (id_sala) REFERENCES sala_comum(id_sala),
    CONSTRAINT fk_consumivel FOREIGN KEY (id_consumivel) REFERENCES consumivel(id_consumivel)
);

CREATE TABLE habilidade_criatura (
    id_habilidade_criatura_pk INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_monstro_simples INT,
    id_boss INT,
    id_habilidade_ataque INT,
    id_habilidade_cura INT,
    id_habilidade_defesa INT,
    CONSTRAINT fk_monstro_simples_hab FOREIGN KEY (id_monstro_simples) REFERENCES monstro_simples(id_monstro_simples),
    CONSTRAINT fk_boss_hab FOREIGN KEY (id_boss) REFERENCES boss(id_boss),
    CONSTRAINT fk_habilidad_ataque FOREIGN KEY (id_habilidade_ataque) REFERENCES Ataque(id_ataque_habilidade), -- Referencia o novo PK
    CONSTRAINT fk_habilidad_cura FOREIGN KEY (id_habilidade_cura) REFERENCES Cura(id_cura_habilidade),       -- Referencia o novo PK
    CONSTRAINT fk_habilidad_defesa FOREIGN KEY (id_habilidade_defesa) REFERENCES Defesa(id_defesa_habilidade), -- Referencia o novo PK
    CONSTRAINT chk_criatura_type_hab CHECK (
       (id_monstro_simples IS NOT NULL AND id_boss IS NULL) OR (id_monstro_simples IS NULL AND id_boss IS NOT NULL)
    ),
    CONSTRAINT chk_habilidade_type CHECK (
      (CASE WHEN id_habilidade_ataque IS NOT NULL THEN 1 ELSE 0 END +
       CASE WHEN id_habilidade_cura IS NOT NULL THEN 1 ELSE 0 END +
       CASE WHEN id_habilidade_defesa IS NOT NULL THEN 1 ELSE 0 END) = 1
    )
);


-- DDL Corrigido para habilidade_estudante
CREATE TABLE habilidade_estudante (
    id_estudante_habilidade_pk INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, -- Novo PK
    id_estudante INT NOT NULL,
    id_habilidade_ataque INT,   -- Referencia Ataque específico
    id_habilidade_cura INT,    -- Referencia Cura específica
    id_habilidade_defesa INT,  -- Referencia Defesa específica
    CONSTRAINT fk_estudante_hab FOREIGN KEY (id_estudante) REFERENCES estudante(id_estudante),
    CONSTRAINT fk_habilidad_ataque_est FOREIGN KEY (id_habilidade_ataque) REFERENCES Ataque(id_ataque_habilidade),
    CONSTRAINT fk_habilidad_cura_est FOREIGN KEY (id_habilidade_cura) REFERENCES Cura(id_cura_habilidade),
    CONSTRAINT fk_habilidad_defesa_est FOREIGN KEY (id_habilidade_defesa) REFERENCES Defesa(id_defesa_habilidade),
    CONSTRAINT chk_habilidade_estudante_type CHECK (
        (CASE WHEN id_habilidade_ataque IS NOT NULL THEN 1 ELSE 0 END +
         CASE WHEN id_habilidade_cura IS NOT NULL THEN 1 ELSE 0 END +
         CASE WHEN id_habilidade_defesa IS NOT NULL THEN 1 ELSE 0 END) = 1
    )
);

-- DDL Corrigido para habilidade_loja
CREATE TABLE habilidade_loja (
    id_loja_habilidade_pk INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, -- Novo PK
    id_loja INT NOT NULL, -- Este é o id_sala da sala_comum
    id_habilidade_ataque INT,   -- Referencia Ataque específico
    id_habilidade_cura INT,    -- Referencia Cura específica
    id_habilidade_defesa INT,  -- Referencia Defesa específica
    CONSTRAINT fk_loja_hab FOREIGN KEY (id_loja) REFERENCES sala_comum(id_sala),
    CONSTRAINT fk_habilidad_ataque_loj FOREIGN KEY (id_habilidade_ataque) REFERENCES Ataque(id_ataque_habilidade),
    CONSTRAINT fk_habilidad_cura_loj FOREIGN KEY (id_habilidade_cura) REFERENCES Cura(id_cura_habilidade),
    CONSTRAINT fk_habilidad_defesa_loj FOREIGN KEY (id_habilidade_defesa) REFERENCES Defesa(id_defesa_habilidade),
    CONSTRAINT chk_habilidade_loja_type CHECK (
        (CASE WHEN id_habilidade_ataque IS NOT NULL THEN 1 ELSE 0 END +
         CASE WHEN id_habilidade_cura IS NOT NULL THEN 1 ELSE 0 END +
         CASE WHEN id_habilidade_defesa IS NOT NULL THEN 1 ELSE 0 END) = 1
    )
);

-- DDL Corrigido para instancia_de_item (mesma lógica que loja_item)
CREATE TABLE instancia_de_item (
    id_instanciaItem INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, -- PK simples
    id_consumivel INT,
    id_equipavel INT,
    id_monetario INT,
    id_reliquia INT,
    id_sala INT,
    id_estudante INT,
    CONSTRAINT fk_consumivel FOREIGN KEY (id_consumivel) REFERENCES consumivel(id_consumivel),
    CONSTRAINT fk_equipavel FOREIGN KEY (id_equipavel) REFERENCES equipavel(id_equipavel),
    CONSTRAINT fk_monetario FOREIGN KEY (id_monetario) REFERENCES monetario(id_monetario),
    CONSTRAINT fk_reliquia FOREIGN KEY (id_reliquia) REFERENCES reliquia(id_reliquia),
    CONSTRAINT fk_id_sala FOREIGN KEY (id_sala) REFERENCES sala_comum(id_sala),
    CONSTRAINT fk_id_estudante FOREIGN KEY (id_estudante) REFERENCES estudante(id_estudante),
    CONSTRAINT chk_one_item_type_instance CHECK (
        (CASE WHEN id_consumivel IS NOT NULL THEN 1 ELSE 0 END +
         CASE WHEN id_equipavel IS NOT NULL THEN 1 ELSE 0 END +
         CASE WHEN id_monetario IS NOT NULL THEN 1 ELSE 0 END +
         CASE WHEN id_reliquia IS NOT NULL THEN 1 ELSE 0 END) = 1
    )
);