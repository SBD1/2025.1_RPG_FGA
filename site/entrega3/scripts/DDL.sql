
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
    preco INT NOT NULL,  -- <<-- COLUNA ADICIONADA
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
    preco INT NOT NULL,  -- <<-- COLUNA ADICIONADA
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
    preco INT NOT NULL,  -- <<-- COLUNA ADICIONADA
    CONSTRAINT fk_id_habilidade FOREIGN KEY (id_habilidade) REFERENCES tipoHabilidade(id_habilidade),
    CONSTRAINT fk_id_tema FOREIGN KEY (id_tema) REFERENCES tema(id_tema)
);

ALTER TABLE instancia_de_item
ADD COLUMN equipado BOOLEAN DEFAULT FALSE;

CREATE OR REPLACE FUNCTION atualiza_equipado_apos_tipoitem_update()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.item_tipo <> OLD.item_tipo THEN
        -- Se mudou de Equipável para outro tipo, seta equipado para NULL
        IF OLD.item_tipo = 'Equipável' AND NEW.item_tipo <> 'Equipável' THEN
            UPDATE instancia_de_item
            SET equipado = NULL
            WHERE id_item = NEW.id_item;
        
        -- Se mudou de outro tipo para Equipável, seta equipado para FALSE
        ELSIF OLD.item_tipo <> 'Equipável' AND NEW.item_tipo = 'Equipável' THEN
            UPDATE instancia_de_item
            SET equipado = FALSE
            WHERE id_item = NEW.id_item;
        END IF;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Cria o trigger para chamar a função após UPDATE no tipo_item
CREATE TRIGGER trg_atualiza_equipado_tipoitem
AFTER UPDATE OF item_tipo ON tipo_item
FOR EACH ROW
EXECUTE FUNCTION atualiza_equipado_apos_tipoitem_update();


CREATE OR REPLACE PROCEDURE criar_estudante(
    p_nome CHAR(100),
    p_vida INT,
    p_estresse INT,
    p_dinheiro INT,
    p_id_sala INT
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_id_estudante INT;
BEGIN
    -- Verifica se a sala existe
    IF NOT EXISTS (SELECT 1 FROM sala_comum WHERE id_sala = p_id_sala) THEN
        RAISE EXCEPTION 'Sala com id % não existe.', p_id_sala;
    END IF;

    -- Insere o estudante
    INSERT INTO estudante (nome, vida, estresse, total_dinheiro, id_sala)
    VALUES (p_nome, p_vida, p_estresse, p_dinheiro, p_id_sala)
    RETURNING id_estudante INTO v_id_estudante;

    -- Inicializa afinidades com todos os temas
    INSERT INTO afinidade (id_estudante, id_tema, xp_atual, nivel_atual)
    SELECT v_id_estudante, id_tema, 0, 1 FROM tema;

    RAISE NOTICE 'Estudante criado com id % e afinidades configuradas.', v_id_estudante;
END;
$$;

-- registro de vitoria monstro
CREATE OR REPLACE PROCEDURE registrar_vitoria_monstro(
    p_id_estudante INT,
    p_id_monstro INT
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_tema_id INT;
    v_xp_ganho INT;
    v_moedas INT;
    v_xp_atual INT;
    v_nivel_atual INT;
BEGIN
    -- Obtém o tema do monstro via habilidades
    SELECT COALESCE(a.id_tema, c.id_tema, d.id_tema)
    INTO v_tema_id
    FROM habilidade_criatura hc
    LEFT JOIN Ataque a ON hc.id_habilidade = a.id_habilidade
    LEFT JOIN Cura c ON hc.id_habilidade = c.id_habilidade
    LEFT JOIN Defesa d ON hc.id_habilidade = d.id_habilidade
    WHERE hc.id_criatura = p_id_monstro
    LIMIT 1;

    -- XP e moedas do monstro
    SELECT xp_tema, qtd_moedas INTO v_xp_ganho, v_moedas
    FROM monstro_simples
    WHERE id_criatura = p_id_monstro;

    -- XP atual
    SELECT xp_atual, nivel_atual INTO v_xp_atual, v_nivel_atual
    FROM afinidade
    WHERE id_estudante = p_id_estudante AND id_tema = v_tema_id;

    -- Atualiza XP e nível
    v_xp_atual := v_xp_atual + v_xp_ganho;
    WHILE v_xp_atual >= v_nivel_atual * 100 LOOP
        v_xp_atual := v_xp_atual - v_nivel_atual * 100;
        v_nivel_atual := v_nivel_atual + 1;
    END LOOP;

    UPDATE afinidade
    SET xp_atual = v_xp_atual, nivel_atual = v_nivel_atual
    WHERE id_estudante = p_id_estudante AND id_tema = v_tema_id;

    -- Atualiza moedas
    UPDATE estudante
    SET total_dinheiro = total_dinheiro + v_moedas
    WHERE id_estudante = p_id_estudante;
END;
$$;

-- dropa reliquia boss
CREATE OR REPLACE PROCEDURE dropar_reliquia_boss(
    p_id_estudante INT,
    p_id_boss INT
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_id_reliquia INT;
    v_ja_possui BOOLEAN;
BEGIN
    -- Obtém relíquia do boss
    SELECT id_reliquia INTO v_id_reliquia
    FROM boss
    WHERE id_criatura = p_id_boss;

    IF v_id_reliquia IS NULL THEN
        RAISE EXCEPTION 'Boss com id % não possui relíquia.', p_id_boss;
    END IF;

    -- Verifica posse
    SELECT EXISTS (
        SELECT 1 FROM instancia_de_item
        WHERE id_estudante = p_id_estudante AND id_item = v_id_reliquia
    ) INTO v_ja_possui;

    IF v_ja_possui THEN
        RAISE NOTICE 'Estudante % já possui a relíquia %.', p_id_estudante, v_id_reliquia;
        RETURN;
    END IF;

    -- Entrega relíquia
    INSERT INTO instancia_de_item (id_item, id_estudante)
    VALUES (v_id_reliquia, p_id_estudante);

    RAISE NOTICE 'Relíquia % entregue ao estudante %.', v_id_reliquia, p_id_estudante;
END;
$$;

-- valida sala de estudante
CREATE OR REPLACE FUNCTION validar_sala_estudante()
RETURNS TRIGGER AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM sala_comum WHERE id_sala = NEW.id_sala) THEN
        RAISE EXCEPTION 'A sala com id % não existe.', NEW.id_sala;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_valida_sala_estudante
BEFORE INSERT OR UPDATE ON estudante
FOR EACH ROW
EXECUTE FUNCTION validar_sala_estudante();


-- checagem de criatura unica
CREATE OR REPLACE FUNCTION check_criatura_unica()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM boss WHERE id_criatura = NEW.id_criatura)
       AND TG_TABLE_NAME = 'monstro_simples' THEN
        RAISE EXCEPTION 'Essa criatura já é um boss. Não pode ser monstro simples.';
    ELSIF EXISTS (SELECT 1 FROM monstro_simples WHERE id_criatura = NEW.id_criatura)
       AND TG_TABLE_NAME = 'boss' THEN
        RAISE EXCEPTION 'Essa criatura já é um monstro simples. Não pode ser boss.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_check_criatura_boss
BEFORE INSERT OR UPDATE ON boss
FOR EACH ROW EXECUTE FUNCTION check_criatura_unica();

CREATE TRIGGER trg_check_criatura_monstro
BEFORE INSERT OR UPDATE ON monstro_simples
FOR EACH ROW EXECUTE FUNCTION check_criatura_unica();


-- checagem de item
CREATE OR REPLACE FUNCTION check_item_equipavel()
RETURNS TRIGGER AS $$
DECLARE
    v_tipo CHAR(10);
BEGIN
    SELECT item_tipo INTO v_tipo
    FROM tipo_item
    WHERE id_item = NEW.id_item;

    IF v_tipo <> 'Equipável' AND NEW.equipado IS NOT NULL THEN
        RAISE EXCEPTION 'Apenas itens equipáveis podem ter valor em "equipado".';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_check_equipado

CREATE OR REPLACE PROCEDURE usar_item_consumivel(p_id_estudante INT, p_id_item INT)
LANGUAGE plpgsql
AS $$
DECLARE
    v_efeito FLOAT;
    v_vida_atual INT;
BEGIN
    -- Verifica se o item é consumível
    IF NOT EXISTS (
        SELECT 1 FROM consumivel WHERE id_item = p_id_item
    ) THEN
        RAISE EXCEPTION 'O item % não é consumível ou não existe.', p_id_item;
    END IF;

    -- Pega o efeito do item
    SELECT efeito INTO v_efeito FROM consumivel WHERE id_item = p_id_item;

    -- Pega vida atual
    SELECT vida INTO v_vida_atual FROM estudante WHERE id_estudante = p_id_estudante;

    -- Aplica o efeito (cura)
    UPDATE estudante
    SET vida = LEAST(v_vida_atual + v_efeito, 100)
    WHERE id_estudante = p_id_estudante;

    -- Remove o item consumido
    DELETE FROM instancia_de_item
    WHERE id_item = p_id_item AND id_estudante = p_id_estudante
    LIMIT 1; -- se tiver mais de um item igual, remove só um

    RAISE NOTICE 'Item % usado. % pontos de vida recuperados.', p_id_item, v_efeito;
END;
$$;

BEFORE INSERT OR UPDATE ON instancia_de_item
FOR EACH ROW EXECUTE FUNCTION check_item_equipavel();

-- 
