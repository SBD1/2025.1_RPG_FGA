
-- criar estudante
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
BEFORE INSERT OR UPDATE ON instancia_de_item
FOR EACH ROW EXECUTE FUNCTION check_item_equipavel();

-- 
