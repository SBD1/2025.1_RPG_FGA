
# Triggers e Procedures no RPG-FGA

Neste sistema de RPG acadêmico, o banco de dados é a parte ativa das **regras de jogo**. Para garantir integridade, automação e lógica de gameplay, usamos **Stored Procedures** e **Triggers**.

---

## Triggers: Regras Automáticas

Triggers são blocos de código que **executam automaticamente** quando certas ações acontecem (INSERT, UPDATE, DELETE). Elas são úteis para:

- **Validar integridade dos dados** (ex: sala deve existir antes de cadastrar um estudante)
- **Evitar estados inválidos** (ex: uma criatura não pode ser boss e monstro ao mesmo tempo)
- **Aplicar restrições sem depender do front-end**

### Exemplos:
- `trg_valida_sala_estudante`: impede cadastrar estudante em sala inexistente
- `trg_check_criatura_boss`: garante unicidade entre boss e monstro
- `trg_check_equipado`: impede itens não-equipáveis de serem marcados como "equipado"

---

## Procedures: Ações Complexas

Stored Procedures são **funções armazenadas** que encapsulam lógicas de jogo reutilizáveis, podendo ser chamadas sob demanda.

### Exemplos:
- `criar_estudante`: cria um novo jogador e inicializa afinidades
- `registrar_vitoria_monstro`: atualiza XP e moedas ao vencer um monstro
- `dropar_reliquia_boss`: entrega uma relíquia única ao derrotar um boss
- `usar_item_consumivel`: aplica efeito de cura e remove o item do inventário

---

## Benefícios no jogo

- **Regras de negócio centralizadas** e seguras no banco
- **Automação da lógica do jogo** (como XP, níveis, uso de itens)
- **Redução de código repetido** no backend ou frontend
- **Facilidade de testes e manutenção**


## Procedure: `criar_estudante`

Cria um novo estudante e inicializa suas afinidades com todos os temas disponíveis.

```sql
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
    IF NOT EXISTS (SELECT 1 FROM sala_comum WHERE id_sala = p_id_sala) THEN
        RAISE EXCEPTION 'Sala com id % não existe.', p_id_sala;
    END IF;

    INSERT INTO estudante (nome, vida, estresse, total_dinheiro, id_sala)
    VALUES (p_nome, p_vida, p_estresse, p_dinheiro, p_id_sala)
    RETURNING id_estudante INTO v_id_estudante;

    INSERT INTO afinidade (id_estudante, id_tema, xp_atual, nivel_atual)
    SELECT v_id_estudante, id_tema, 0, 1 FROM tema;

    RAISE NOTICE 'Estudante criado com id % e afinidades configuradas.', v_id_estudante;
END;
$$;
```

## Procedure: `registrar_vitoria_monstro`

Registra XP e moedas ao derrotar um monstro.

```sql
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
    SELECT COALESCE(a.id_tema, c.id_tema, d.id_tema)
    INTO v_tema_id
    FROM habilidade_criatura hc
    LEFT JOIN Ataque a ON hc.id_habilidade = a.id_habilidade
    LEFT JOIN Cura c ON hc.id_habilidade = c.id_habilidade
    LEFT JOIN Defesa d ON hc.id_habilidade = d.id_habilidade
    WHERE hc.id_criatura = p_id_monstro
    LIMIT 1;

    SELECT xp_tema, qtd_moedas INTO v_xp_ganho, v_moedas
    FROM monstro_simples
    WHERE id_criatura = p_id_monstro;

    SELECT xp_atual, nivel_atual INTO v_xp_atual, v_nivel_atual
    FROM afinidade
    WHERE id_estudante = p_id_estudante AND id_tema = v_tema_id;

    v_xp_atual := v_xp_atual + v_xp_ganho;
    WHILE v_xp_atual >= v_nivel_atual * 100 LOOP
        v_xp_atual := v_xp_atual - v_nivel_atual * 100;
        v_nivel_atual := v_nivel_atual + 1;
    END LOOP;

    UPDATE afinidade
    SET xp_atual = v_xp_atual, nivel_atual = v_nivel_atual
    WHERE id_estudante = p_id_estudante AND id_tema = v_tema_id;

    UPDATE estudante
    SET total_dinheiro = total_dinheiro + v_moedas
    WHERE id_estudante = p_id_estudante;
END;
$$;
```

## Procedure: `dropar_reliquia_boss`

Entrega a relíquia do boss se o estudante ainda não a tiver.

```sql
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
    SELECT id_reliquia INTO v_id_reliquia
    FROM boss
    WHERE id_criatura = p_id_boss;

    IF v_id_reliquia IS NULL THEN
        RAISE EXCEPTION 'Boss com id % não possui relíquia.', p_id_boss;
    END IF;

    SELECT EXISTS (
        SELECT 1 FROM instancia_de_item
        WHERE id_estudante = p_id_estudante AND id_item = v_id_reliquia
    ) INTO v_ja_possui;

    IF v_ja_possui THEN
        RAISE NOTICE 'Estudante % já possui a relíquia %.', p_id_estudante, v_id_reliquia;
        RETURN;
    END IF;

    INSERT INTO instancia_de_item (id_item, id_estudante)
    VALUES (v_id_reliquia, p_id_estudante);

    RAISE NOTICE 'Relíquia % entregue ao estudante %.', v_id_reliquia, p_id_estudante;
END;
$$;
```
## Trigger: `validar_sala_estudante`

Impede inserção de estudante em sala inexistente.

```sql
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
```

---

## Trigger: `check_criatura_unica`

Garante que uma criatura não seja ao mesmo tempo boss e monstro.

```sql
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
FOR EACH ROW
EXECUTE FUNCTION check_criatura_unica();

CREATE TRIGGER trg_check_criatura_monstro
BEFORE INSERT OR UPDATE ON monstro_simples
FOR EACH ROW
EXECUTE FUNCTION check_criatura_unica();
```

---

## Trigger: `check_item_equipavel`

Garante que somente itens do tipo "Equipável" possam ter o campo `equipado`.

```sql
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
FOR EACH ROW
EXECUTE FUNCTION check_item_equipavel();
```
