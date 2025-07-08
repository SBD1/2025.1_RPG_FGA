# DML

DML (Data Manipulation Language) é a parte da linguagem SQL usada para inserir, atualizar, deletar e manipular dados dentro das tabelas de um banco de dados.

Neste contexto, o script `DML.sql` foi utilizado para popular o banco de dados com dados iniciais, simulando um ambiente completo de um RPG acadêmico baseado em temas universitários da Universidade de Brasília (UnB);

## Operações realizadas

## Inserções na tabela **tema**

```sql
-- Populando tabela 'tema' 
INSERT INTO tema (nome) VALUES
('Matemática'),
('Programação'),
('Engenharias'),
('Humanidades'),
('Gerais');
```

---

## Inserções de **tipoHabilidade** e **Ataque**

```sql
-- Populando 'tipoHabilidade' e 'Ataque'
-- Habilidades de Matemática
INSERT INTO tipoHabilidade (tipo_habilidade) VALUES ('ataque'); -- ID 1
INSERT INTO Ataque (id_habilidade, id_tema, nome, nivel, coolDown, danoCausado, preco) VALUES (1, 1, 'Equação Quadrática', 5, 2, 15, 40);
INSERT INTO tipoHabilidade (tipo_habilidade) VALUES ('ataque'); -- ID 2
INSERT INTO Ataque (id_habilidade, id_tema, nome, nivel, coolDown, danoCausado, preco) VALUES (2, 1, 'Teorema de Pitágoras', 8, 3, 20, 60);
INSERT INTO tipoHabilidade (tipo_habilidade) VALUES ('ataque'); -- ID 3
INSERT INTO Ataque (id_habilidade, id_tema, nome, nivel, coolDown, danoCausado, preco) VALUES (3, 1, 'Cálculo Integral', 15, 5, 30, 105);
-- Habilidades de Programação
INSERT INTO tipoHabilidade (tipo_habilidade) VALUES ('ataque'); -- ID 4
INSERT INTO Ataque (id_habilidade, id_tema, nome, nivel, coolDown, danoCausado, preco) VALUES (4, 2, 'Bug Report', 6, 2, 16, 46);
INSERT INTO tipoHabilidade (tipo_habilidade) VALUES ('ataque'); -- ID 5
INSERT INTO Ataque (id_habilidade, id_tema, nome, nivel, coolDown, danoCausado, preco) VALUES (5, 2, 'Debug Rápido', 10, 3, 22, 72);
INSERT INTO tipoHabilidade (tipo_habilidade) VALUES ('ataque'); -- ID 6 
INSERT INTO Ataque (id_habilidade, id_tema, nome, nivel, coolDown, danoCausado, preco) VALUES (6, 2, 'Zero Division', 18, 6, 35, 125);
-- Habilidades de Engenharias
INSERT INTO tipoHabilidade (tipo_habilidade) VALUES ('ataque'); -- ID 7
INSERT INTO Ataque (id_habilidade, id_tema, nome, nivel, coolDown, danoCausado, preco) VALUES (7, 3, 'Desenho Técnico', 7, 2, 18, 53);
INSERT INTO tipoHabilidade (tipo_habilidade) VALUES ('ataque'); -- ID 8
INSERT INTO Ataque (id_habilidade, id_tema, nome, nivel, coolDown, danoCausado, preco) VALUES (8, 3, 'Análise Estrutural', 12, 4, 25, 85);
INSERT INTO tipoHabilidade (tipo_habilidade) VALUES ('ataque'); -- ID 9
INSERT INTO Ataque (id_habilidade, id_tema, nome, nivel, coolDown, danoCausado, preco) VALUES (9, 3, 'Falha de Projeto', 17, 5, 32, 117);
-- Habilidades de Humanidades
INSERT INTO tipoHabilidade (tipo_habilidade) VALUES ('ataque'); -- ID 10
INSERT INTO Ataque (id_habilidade, id_tema, nome, nivel, coolDown, danoCausado, preco) VALUES (10, 4, 'Retórica Persuasiva', 5, 2, 14, 39);
INSERT INTO tipoHabilidade (tipo_habilidade) VALUES ('ataque'); -- ID 11
INSERT INTO Ataque (id_habilidade, id_tema, nome, nivel, coolDown, danoCausado, preco) VALUES (11, 4, 'Crítica Social', 9, 3, 19, 64);
INSERT INTO tipoHabilidade (tipo_habilidade) VALUES ('ataque'); -- ID 12
INSERT INTO Ataque (id_habilidade, id_tema, nome, nivel, coolDown, danoCausado, preco) VALUES (12, 4, 'Argumento Irrefutável', 16, 5, 28, 108);
-- Habilidades Gerais
INSERT INTO tipoHabilidade (tipo_habilidade) VALUES ('ataque'); -- ID 13
INSERT INTO Ataque (id_habilidade, id_tema, nome, nivel, coolDown, danoCausado, preco) VALUES (13, 5, 'Ataque Básico', 1, 1, 8, 13);
INSERT INTO tipoHabilidade (tipo_habilidade) VALUES ('ataque'); -- ID 14
INSERT INTO Ataque (id_habilidade, id_tema, nome, nivel, coolDown, danoCausado, preco) VALUES (14, 5, 'Estudo Avançado', 10, 4, 20, 70);
```

---

## Inserções de **tipoHabilidade** e **Cura**

```sql
-- Populando 'tipoHabilidade' e 'Cura'
INSERT INTO tipoHabilidade (tipo_habilidade) VALUES ('cura'); -- ID 15
INSERT INTO Cura (id_habilidade, id_tema, nome, nivel, coolDown, vidaRecuperada, preco) VALUES (15, 1, 'Revisão de Conceitos', 4, 3, 10, 30);
INSERT INTO tipoHabilidade (tipo_habilidade) VALUES ('cura'); -- ID 16
INSERT INTO Cura (id_habilidade, id_tema, nome, nivel, coolDown, vidaRecuperada, preco) VALUES (16, 2, 'Stack Overflow', 5, 3, 12, 37);
INSERT INTO tipoHabilidade (tipo_habilidade) VALUES ('cura'); -- ID 17
INSERT INTO Cura (id_habilidade, id_tema, nome, nivel, coolDown, vidaRecuperada, preco) VALUES (17, 3, 'Reparo de Circuito', 6, 3, 11, 41);
INSERT INTO tipoHabilidade (tipo_habilidade) VALUES ('cura'); -- ID 18
INSERT INTO Cura (id_habilidade, id_tema, nome, nivel, coolDown, vidaRecuperada, preco) VALUES (18, 4, 'Sessão de Terapia', 4, 3, 9, 29);
INSERT INTO tipoHabilidade (tipo_habilidade) VALUES ('cura'); -- ID 19
INSERT INTO Cura (id_habilidade, id_tema, nome, nivel, coolDown, vidaRecuperada, preco) VALUES (19, 5, 'Curativo Simples', 1, 1, 5, 10);
INSERT INTO tipoHabilidade (tipo_habilidade) VALUES ('cura'); -- ID 20
INSERT INTO Cura (id_habilidade, id_tema, nome, nivel, coolDown, vidaRecuperada, preco) VALUES (20, 5, 'Pausa para o Café', 7, 2, 15, 50);
```

---

## Inserções de **tipoHabilidade** e **Defesa**

```sql
-- Populando 'tipoHabilidade' e 'Defesa'
INSERT INTO tipoHabilidade (tipo_habilidade) VALUES ('defesa'); -- ID 21
INSERT INTO Defesa (id_habilidade, id_tema, nome, nivel, coolDown, danoMitigado, preco) VALUES (21, 1, 'Defesa Numérica', 7, 2, 10, 45);
INSERT INTO tipoHabilidade (tipo_habilidade) VALUES ('defesa'); -- ID 22
INSERT INTO Defesa (id_habilidade, id_tema, nome, nivel, coolDown, danoMitigado, preco) VALUES (22, 2, 'Firewall Pessoal', 9, 2, 13, 58);
INSERT INTO tipoHabilidade (tipo_habilidade) VALUES ('defesa'); -- ID 23
INSERT INTO Defesa (id_habilidade, id_tema, nome, nivel, coolDown, danoMitigado, preco) VALUES (23, 3, 'Material Resistente', 8, 2, 11, 51);
INSERT INTO tipoHabilidade (tipo_habilidade) VALUES ('defesa'); -- ID 24
INSERT INTO Defesa (id_habilidade, id_tema, nome, nivel, coolDown, danoMitigado, preco) VALUES (24, 4, 'Escudo Cultural', 7, 2, 9, 44);
INSERT INTO tipoHabilidade (tipo_habilidade) VALUES ('defesa'); -- ID 25
INSERT INTO Defesa (id_habilidade, id_tema, nome, nivel, coolDown, danoMitigado, preco) VALUES (25, 5, 'Corrida Rápida', 2, 1, 7, 17);
INSERT INTO tipoHabilidade (tipo_habilidade) VALUES ('defesa'); -- ID 26
INSERT INTO Defesa (id_habilidade, id_tema, nome, nivel, coolDown, danoMitigado, preco) VALUES (26, 5, 'Concentração Total', 11, 3, 14, 69);
```

---

## Inserções na tabela **tipo_item**

```sql
-- Populando 'tipo_item'
INSERT INTO tipo_item (item_tipo) VALUES
('Relíquia'), ('Relíquia'), ('Relíquia'), ('Relíquia'), ('Relíquia'), -- IDs 1-5
('Consumível'), ('Consumível'), ('Consumível'), ('Consumível'), ('Consumível'), -- IDs 6-10
('Equipável'), ('Equipável'), ('Equipável'), -- IDs 11-13
('Monetário'), ('Monetário'); -- IDs 14-15
```

---

## Inserções na tabela **reliquia**

```sql
-- Populando 'reliquia'
INSERT INTO reliquia (id_reliquia, nome, descricao, tipo_reliquia) VALUES
(1, 'Cálculo Infinito', 'Relíquia do tema Matemática', 'Cálculo Infinito'),
(2, 'Código Fonte Universal', 'Relíquia do tema Programação', 'Código Fonte Universal'),
(3, 'Projeto Mestre', 'Relíquia do tema Engenharias', 'Projeto Mestre'),
(4, 'Sabedoria Ancestral', 'Relíquia do tema Humanidades', 'Sabedoria Ancestral'),
(5, 'Conhecimento Geral Abrangente', 'Relíquia do tema Gerais', 'Conhecimento Geral Abrangente');
```

---

## Inserções de **tipo_criatura** e **monstro_simples**

```sql
-- Populando 'tipo_criatura' e 'monstro_simples'
INSERT INTO tipo_criatura (tipo_criatura) VALUES ('Monstro'); -- ID 1
INSERT INTO monstro_simples (id_criatura, nome, descricao, nivel, vida_max, xp_tema, qtd_moedas) VALUES (1, 'Erro de Sintaxe', 'Um pequeno erro que atrapalha o código.', 3, 30, 5, 2);
INSERT INTO tipo_criatura (tipo_criatura) VALUES ('Monstro'); -- ID 2
INSERT INTO monstro_simples (id_criatura, nome, descricao, nivel, vida_max, xp_tema, qtd_moedas) VALUES (2, 'Derivada Confusa', 'Uma função matemática que parece não ter fim.', 5, 45, 7, 3);
INSERT INTO tipo_criatura (tipo_criatura) VALUES ('Monstro'); -- ID 3
INSERT INTO monstro_simples (id_criatura, nome, descricao, nivel, vida_max, xp_tema, qtd_moedas) VALUES (3, 'Plágio Descarado', 'Uma ameaça à originalidade acadêmica.', 7, 60, 9, 4);
INSERT INTO tipo_criatura (tipo_criatura) VALUES ('Monstro'); -- ID 4
INSERT INTO monstro_simples (id_criatura, nome, descricao, nivel, vida_max, xp_tema, qtd_moedas) VALUES (4, 'Fio Solto', 'Um defeito simples em uma instalação elétrica.', 4, 35, 6, 2);
INSERT INTO tipo_criatura (tipo_criatura) VALUES ('Monstro'); -- ID 5
INSERT INTO monstro_simples (id_criatura, nome, descricao, nivel, vida_max, xp_tema, qtd_moedas) VALUES (5, 'Preguiça Matinal', 'A força que impede o estudante de levantar.', 6, 50, 8, 3);
INSERT INTO tipo_criatura (tipo_criatura) VALUES ('Monstro'); -- ID 6
INSERT INTO monstro_simples (id_criatura, nome, descricao, nivel, vida_max, xp_tema, qtd_moedas) VALUES (6, 'Loop Infinito', 'Um programa que nunca termina.', 9, 70, 12, 5);
INSERT INTO tipo_criatura (tipo_criatura) VALUES ('Monstro'); -- ID 7
INSERT INTO monstro_simples (id_criatura, nome, descricao, nivel, vida_max, xp_tema, qtd_moedas) VALUES (7, 'Paradoxo Lógico', 'Um problema que desafia a razão.', 11, 85, 15, 6);
INSERT INTO tipo_criatura (tipo_criatura) VALUES ('Monstro'); -- ID 8
INSERT INTO monstro_simples (id_criatura, nome, descricao, nivel, vida_max, xp_tema, qtd_moedas) VALUES (8, 'Teoria da Conspiração', 'Uma narrativa sem evidências, mas persistente.', 13, 100, 18, 7);
INSERT INTO tipo_criatura (tipo_criatura) VALUES ('Monstro'); -- ID 9
INSERT INTO monstro_simples (id_criatura, nome, descricao, nivel, vida_max, xp_tema, qtd_moedas) VALUES (9, 'Solda Fria', 'Uma conexão mal feita que causa instabilidade.', 10, 75, 13, 5);
INSERT INTO tipo_criatura (tipo_criatura) VALUES ('Monstro'); -- ID 10
INSERT INTO monstro_simples (id_criatura, nome, descricao, nivel, vida_max, xp_tema, qtd_moedas) VALUES (10, 'Distração Coletiva', 'O inimigo de toda sessão de estudos.', 8, 65, 10, 4);
```

---

## Inserções de **tipo_criatura** e **boss**

```sql
-- Populando 'tipo_criatura' e 'boss'
INSERT INTO tipo_criatura (tipo_criatura) VALUES ('Boss'); -- ID 11
INSERT INTO boss (id_criatura, nome, descricao, nivel, vida_max, id_reliquia) VALUES (11, 'Chicão', 'Gêmeo maligno que nega todas as matriculas.', 20, 200, 1);
INSERT INTO tipo_criatura (tipo_criatura) VALUES ('Boss'); -- ID 12
INSERT INTO boss (id_criatura, nome, descricao, nivel, vida_max, id_reliquia) VALUES (12, 'Frango assado do RU', 'Vai te dar uma intoxicação alimentar, pois está sempre cru.', 20, 250, 2);
INSERT INTO tipo_criatura (tipo_criatura) VALUES ('Boss'); -- ID 13
INSERT INTO boss (id_criatura, nome, descricao, nivel, vida_max, id_reliquia) VALUES (13, 'Superlotação', 'Esse curso não precisa de mais uma aluno...', 20, 260, 4);
INSERT INTO tipo_criatura (tipo_criatura) VALUES ('Boss'); -- ID 14
INSERT INTO boss (id_criatura, nome, descricao, nivel, vida_max, id_reliquia) VALUES (14, 'Thinkpad do mocap', 'É um ser ancestral que vai travar quando vc menos esperar.', 20, 230, 3);
INSERT INTO tipo_criatura (tipo_criatura) VALUES ('Boss'); -- ID 15
INSERT INTO boss (id_criatura, nome, descricao, nivel, vida_max, id_reliquia) VALUES (15, 'Mauricio me dá SS', 'Isso mesmo, esse boss sempre dá SS aos alunos, em troca da sua alma, aceitas?.', 20, 190, 5);
```

---

## Inserções na tabela **campus**

```sql
-- Populando tabela 'campus'
INSERT INTO campus (nome, descricao) VALUES
('UnB Campus Gama', 'O coração da jornada acadêmica do RPG-FGA.');
```

---

## Inserções e atualizações da tabela **setor**

```sql
-- Populando tabela 'setor'
INSERT INTO setor (id_campus, nome, descricao) VALUES 
(1, 'UED', 'Unidade de Ensino à Distância, com laboratórios e salas de professores.'),
(1, 'Containers', 'Setor de laboratórios específicos, construídos em containers.'),
(1, 'UAC', 'Unidade Acadêmica Central, com salas numeradas.'),
(1, 'Refeitório Universitário', 'Local de alimentação e descanso para os estudantes.'),
(1, 'Estacionamento', 'Área externa para veículos e um espaço de lazer.'),
(1, 'LDTEA', 'Laboratório de Desenho Técnico e Expressão Artística.');

-- Atualiza id_proxSetor e id_prevSetor
UPDATE setor SET id_proxSetor = 2, id_prevSetor = 6 WHERE id_setor = 1;
UPDATE setor SET id_proxSetor = 3, id_prevSetor = 1 WHERE id_setor = 2;
UPDATE setor SET id_proxSetor = 4, id_prevSetor = 2 WHERE id_setor = 3;
UPDATE setor SET id_proxSetor = 5, id_prevSetor = 3 WHERE id_setor = 4;
UPDATE setor SET id_proxSetor = 6, id_prevSetor = 4 WHERE id_setor = 5;
UPDATE setor SET id_proxSetor = 1, id_prevSetor = 5 WHERE id_setor = 6;
```

---

## Geração de salas (**sala_comum**) – bloco DO

```sql
-- Populando tabela 'sala_comum' com lógica de dungeon corrigida
DO $$
DECLARE
    i INT;
    sector_id INT;
    room_count INT := 10;
    shop_assigned BOOLEAN;
    prev_room_id INT;
    
    -- Lógica para garantir no máximo 5 dungeons, uma por setor
    dungeon_sectors INT[];
    dungeon_room_number INT;
BEGIN
    -- Seleciona 5 setores aleatórios para receber uma dungeon
    SELECT ARRAY(
        SELECT id_setor FROM setor ORDER BY random() LIMIT 5
    ) INTO dungeon_sectors;

    FOR sector_id IN 1..6 LOOP
        shop_assigned := FALSE;
        prev_room_id := NULL;
        
        -- Sorteia em qual sala do setor a dungeon será colocada, caso o setor seja um dos escolhidos
        dungeon_room_number := floor(random() * room_count + 1);

        FOR i IN 1..room_count LOOP
            DECLARE
                room_name CHAR(100);
                room_desc CHAR(255);
                has_shop BOOLEAN := FALSE;
                has_dungeon BOOLEAN := FALSE;
                current_room_id INT;
            BEGIN
                IF NOT shop_assigned AND i = 1 THEN
                    has_shop := TRUE;
                    shop_assigned := TRUE;
                ELSE
                    has_shop := (random() < 0.3);
                END IF;

                IF sector_id = ANY(dungeon_sectors) AND i = dungeon_room_number THEN
                    has_dungeon := TRUE;
                END IF;

                CASE sector_id
                    WHEN 1 THEN room_name := 'Laboratório de Redes ' || i; room_desc := 'Um laboratório de informática focado em redes.';
                    WHEN 2 THEN room_name := 'Laboratório de IoT ' || i; room_desc := 'Um laboratório modular para projetos de Internet das Coisas.';
                    WHEN 3 THEN room_name := 'Sala S-' || i; room_desc := 'Uma sala de aula padrão do UAC.';
                    WHEN 4 THEN room_name := 'Mesa ' || i; room_desc := 'Uma mesa no refeitório, ideal para uma refeição rápida.';
                    WHEN 5 THEN room_name := 'Lote E-' || i; room_desc := 'Um dos lotes do estacionamento do campus.';
                    WHEN 6 THEN room_name := 'Laboratório de Protótipos ' || i; room_desc := 'Um laboratório para criação de protótipos e maquetes.';
                END CASE;

                INSERT INTO sala_comum (id_setor, id_prevSala, nome, descricao, tem_loja, tem_dungeon) VALUES
                (sector_id, prev_room_id, room_name, room_desc, has_shop, has_dungeon)
                RETURNING id_sala INTO current_room_id;

                IF prev_room_id IS NOT NULL THEN
                    UPDATE sala_comum SET id_proxSala = current_room_id WHERE id_sala = prev_room_id;
                END IF;
                prev_room_id := current_room_id;
            END;
        END LOOP;
        
        IF prev_room_id IS NOT NULL THEN
            DECLARE
                first_room_id INT;
            BEGIN
                SELECT id_sala INTO first_room_id FROM sala_comum WHERE id_setor = sector_id ORDER BY id_sala ASC LIMIT 1;
                UPDATE sala_comum SET id_proxSala = first_room_id WHERE id_sala = prev_room_id;
                UPDATE sala_comum SET id_prevSala = prev_room_id WHERE id_sala = first_room_id;
            END;
        END IF;
    END LOOP;
END $$;
```

---

## Inserções na tabela **estudante**

```sql
-- Populando tabela 'estudante'
INSERT INTO estudante (nome, vida, estresse, total_dinheiro, id_sala) VALUES
('Alice Dev', 20, 20, 10, (SELECT id_sala FROM sala_comum WHERE id_setor = 1 ORDER BY id_sala LIMIT 1)),
('Léo Eng', 20, 20, 10, (SELECT id_sala FROM sala_comum WHERE id_setor = 2 ORDER BY id_sala LIMIT 1)),
('Carlos Mat', 20, 20, 10, (SELECT id_sala FROM sala_comum WHERE id_setor = 3 ORDER BY id_sala LIMIT 1)),
('Diana Hum', 20, 20, 10, (SELECT id_sala FROM sala_comum WHERE id_setor = 4 ORDER BY id_sala LIMIT 1)),
('Eduardo G', 20, 20, 10, (SELECT id_sala FROM sala_comum WHERE id_setor = 5 ORDER BY id_sala LIMIT 1));
```

---

## Inserções na tabela **afinidade**

```sql
-- Populando tabela 'afinidade'
INSERT INTO afinidade (id_estudante, id_tema, xp_atual, nivel_atual) VALUES
(1, 1, 0, 1), (1, 2, 0, 1), (1, 3, 0, 1), (1, 4, 0, 1), (1, 5, 0, 1),
(2, 1, 0, 1), (2, 2, 0, 1), (2, 3, 0, 1), (2, 4, 0, 1), (2, 5, 0, 1),
(3, 1, 0, 1), (3, 2, 0, 1), (3, 3, 0, 1), (3, 4, 0, 1), (3, 5, 0, 1),
(4, 1, 0, 1), (4, 2, 0, 1), (4, 3, 0, 1), (4, 4, 0, 1), (4, 5, 0, 1),
(5, 1, 0, 1), (5, 2, 0, 1), (5, 3, 0, 1), (5, 4, 0, 1), (5, 5, 0, 1);
```

---

## Inserções nas tabelas **consumivel**, **equipavel** e **monetario**

```sql
-- Populando 'consumivel'
INSERT INTO consumivel (id_item, nome, descricao, efeito, preco) VALUES
(6, 'Café Expresso', 'Recupera um pouco de estresse e te dá energia.', 5.0, 3.0),
(7, 'Barra de Cereal', 'Um lanche rápido para restaurar a vitalidade.', 10.0, 5.0),
(8, 'Comprimido Analgésico', 'Alivia dores de cabeça e ajuda a focar.', 7.0, 4.0),
(9, 'Guaraná Natural', 'Aumenta sua vida por um curto período.', 15.0, 8.0),
(10, 'Chocolate Acadêmico', 'Melhora o humor e a concentração.', 12.0, 6.0);

-- Populando 'equipavel'
INSERT INTO equipavel (id_item, nome, descricao, efeito, preco) VALUES
(11, 'Óculos de Leitura Avançada', 'Aumenta sua vida máxima permanentemente.', 10, 50),
(12, 'Mochila de Estudo', 'Permite carregar mais itens.', 5, 30),
(13, 'Tênis Confortável', 'Aumenta sua capacidade de fuga em combate.', 2, 40);

-- Populando 'monetario'
INSERT INTO monetario (id_item, nome, descricao, valor) VALUES
(14, 'Moeda Acadêmica', 'A moeda corrente do campus.', 1),
(15, 'Ficha de RU', 'Pode ser trocada por refeições.', 5);
```

---

## Inserções na tabela **dungeon_academica**

```sql
-- Populando tabela 'dungeon_academica'
WITH dungeon_salas AS (
    SELECT id_sala, ROW_NUMBER() OVER (ORDER BY id_sala) as rn
    FROM sala_comum
    WHERE tem_dungeon = TRUE
)
INSERT INTO dungeon_academica (id_dungeon, nome, descricao, id_tema) VALUES
((SELECT id_sala FROM dungeon_salas WHERE rn = 1), 'Matemática Quântica', 'Uma dungeon onde os números se comportam de maneira imprevisível.', 1),
((SELECT id_sala FROM dungeon_salas WHERE rn = 2), 'Labirinto de Códigos', 'Um ambiente complexo cheio de algoritmos e funções enigmáticas.', 2),
((SELECT id_sala FROM dungeon_salas WHERE rn = 3), 'Fundição de Ideias', 'Um lugar onde projetos complexos ganham vida.', 3),
((SELECT id_sala FROM dungeon_salas WHERE rn = 4), 'Debate Filosófico', 'Um salão onde as ideias se chocam e a retórica é a principal arma.', 4),
((SELECT id_sala FROM dungeon_salas WHERE rn = 5), 'O Grande Auditório', 'Um local de conhecimento vasto e diversificado.', 5);
```

---

## Instanciação de criaturas na dungeon – bloco DO

```sql
DO $$
DECLARE
    dungeon_rec RECORD;
    monster_rec RECORD;
BEGIN
    FOR dungeon_rec IN SELECT id_dungeon, id_tema FROM dungeon_academica LOOP
        -- Seleciona 10 monstros aleatórios do mesmo tema da dungeon
        FOR monster_rec IN
            SELECT ms.id_criatura, ms.vida_max
            FROM monstro_simples ms
            WHERE mod(ms.id_criatura, 5) + 1 = dungeon_rec.id_tema
            ORDER BY random()
            LIMIT 10
        LOOP
            INSERT INTO instancia_de_criatura (id_criatura, vida_atual, id_dungeon)
            VALUES (monster_rec.id_criatura, monster_rec.vida_max, dungeon_rec.id_dungeon);
        END LOOP;
    END LOOP;
END $$;
```

---

## Inserções na tabela **loja_item** – bloco DO

```sql
-- Populando tabela 'loja_item'
DO $$
DECLARE
    shop_sala_id INT;
    consumivel_id INT;
BEGIN
    FOR shop_sala_id IN (SELECT id_sala FROM sala_comum WHERE tem_loja = TRUE) LOOP
        FOR consumivel_id IN (SELECT id_item FROM consumivel ORDER BY random() LIMIT 3) LOOP
            INSERT INTO loja_item (id_sala, id_item) VALUES (shop_sala_id, consumivel_id);
        END LOOP;
    END LOOP;
END $$;
```

---

## Inserções na tabela **habilidade_criatura**

```sql
-- Populando tabela 'habilidade_criatura'
INSERT INTO habilidade_criatura (id_criatura, id_habilidade) VALUES
-- Monstros Simples
((SELECT id_criatura FROM monstro_simples WHERE nome = 'Erro de Sintaxe'), (SELECT id_habilidade FROM Ataque WHERE nome = 'Bug Report')),
((SELECT id_criatura FROM monstro_simples WHERE nome = 'Erro de Sintaxe'), (SELECT id_habilidade FROM Ataque WHERE nome = 'Ataque Básico')),
((SELECT id_criatura FROM monstro_simples WHERE nome = 'Derivada Confusa'), (SELECT id_habilidade FROM Ataque WHERE nome = 'Equação Quadrática')),
((SELECT id_criatura FROM monstro_simples WHERE nome = 'Derivada Confusa'), (SELECT id_habilidade FROM Defesa WHERE nome = 'Defesa Numérica')),
((SELECT id_criatura FROM monstro_simples WHERE nome = 'Plágio Descarado'), (SELECT id_habilidade FROM Ataque WHERE nome = 'Retórica Persuasiva')),
((SELECT id_criatura FROM monstro_simples WHERE nome = 'Plágio Descarado'), (SELECT id_habilidade FROM Ataque WHERE nome = 'Crítica Social')),
((SELECT id_criatura FROM monstro_simples WHERE nome = 'Fio Solto'), (SELECT id_habilidade FROM Ataque WHERE nome = 'Desenho Técnico')),
((SELECT id_criatura FROM monstro_simples WHERE nome = 'Fio Solto'), (SELECT id_habilidade FROM Defesa WHERE nome = 'Material Resistente')),
((SELECT id_criatura FROM monstro_simples WHERE nome = 'Preguiça Matinal'), (SELECT id_habilidade FROM Ataque WHERE nome = 'Ataque Básico')),
((SELECT id_criatura FROM monstro_simples WHERE nome = 'Preguiça Matinal'), (SELECT id_habilidade FROM Cura WHERE nome = 'Pausa para o Café')),
((SELECT id_criatura FROM monstro_simples WHERE nome = 'Loop Infinito'), (SELECT id_habilidade FROM Ataque WHERE nome = 'Debug Rápido')),
((SELECT id_criatura FROM monstro_simples WHERE nome = 'Loop Infinito'), (SELECT id_habilidade FROM Defesa WHERE nome = 'Firewall Pessoal')),
((SELECT id_criatura FROM monstro_simples WHERE nome = 'Paradoxo Lógico'), (SELECT id_habilidade FROM Ataque WHERE nome = 'Teorema de Pitágoras')),
((SELECT id_criatura FROM monstro_simples WHERE nome = 'Paradoxo Lógico'), (SELECT id_habilidade FROM Defesa WHERE nome = 'Defesa Numérica')),
((SELECT id_criatura FROM monstro_simples WHERE nome = 'Teoria da Conspiração'), (SELECT id_habilidade FROM Ataque WHERE nome = 'Crítica Social')),
((SELECT id_criatura FROM monstro_simples WHERE nome = 'Teoria da Conspiração'), (SELECT id_habilidade FROM Defesa WHERE nome = 'Escudo Cultural')),
((SELECT id_criatura FROM monstro_simples WHERE nome = 'Solda Fria'), (SELECT id_habilidade FROM Ataque WHERE nome = 'Análise Estrutural')),
((SELECT id_criatura FROM monstro_simples WHERE nome = 'Solda Fria'), (SELECT id_habilidade FROM Cura WHERE nome = 'Reparo de Circuito')),
((SELECT id_criatura FROM monstro_simples WHERE nome = 'Distração Coletiva'), (SELECT id_habilidade FROM Ataque WHERE nome = 'Estudo Avançado')),
((SELECT id_criatura FROM monstro_simples WHERE nome = 'Distração Coletiva'), (SELECT id_habilidade FROM Cura WHERE nome = 'Sessão de Terapia')),
-- Bosses
((SELECT id_criatura FROM boss WHERE nome = 'Chicão'), (SELECT id_habilidade FROM Ataque WHERE nome = 'Cálculo Integral')),
((SELECT id_criatura FROM boss WHERE nome = 'Chicão'), (SELECT id_habilidade FROM Defesa WHERE nome = 'Defesa Numérica')),
((SELECT id_criatura FROM boss WHERE nome = 'Chicão'), (SELECT id_habilidade FROM Cura WHERE nome = 'Revisão de Conceitos')),
((SELECT id_criatura FROM boss WHERE nome = 'Frango assado do RU'), (SELECT id_habilidade FROM Ataque WHERE nome = 'Zero Division')),
((SELECT id_criatura FROM boss WHERE nome = 'Frango assado do RU'), (SELECT id_habilidade FROM Defesa WHERE nome = 'Firewall Pessoal')),
((SELECT id_criatura FROM boss WHERE nome = 'Frango assado do RU'), (SELECT id_habilidade FROM Cura WHERE nome = 'Stack Overflow')),
((SELECT id_criatura FROM boss WHERE nome = 'Superlotação'), (SELECT id_habilidade FROM Ataque WHERE nome = 'Argumento Irrefutável')),
((SELECT id_criatura FROM boss WHERE nome = 'Superlotação'), (SELECT id_habilidade FROM Defesa WHERE nome = 'Escudo Cultural')),
((SELECT id_criatura FROM boss WHERE nome = 'Superlotação'), (SELECT id_habilidade FROM Cura WHERE nome = 'Sessão de Terapia')),
((SELECT id_criatura FROM boss WHERE nome = 'Thinkpad do mocap'), (SELECT id_habilidade FROM Ataque WHERE nome = 'Falha de Projeto')),
((SELECT id_criatura FROM boss WHERE nome = 'Thinkpad do mocap'), (SELECT id_habilidade FROM Defesa WHERE nome = 'Material Resistente')),
((SELECT id_criatura FROM boss WHERE nome = 'Thinkpad do mocap'), (SELECT id_habilidade FROM Cura WHERE nome = 'Reparo de Circuito')),
((SELECT id_criatura FROM boss WHERE nome = 'Mauricio me dá SS'), (SELECT id_habilidade FROM Ataque WHERE nome = 'Estudo Avançado')),
((SELECT id_criatura FROM boss WHERE nome = 'Mauricio me dá SS'), (SELECT id_habilidade FROM Defesa WHERE nome = 'Concentração Total')),
((SELECT id_criatura FROM boss WHERE nome = 'Mauricio me dá SS'), (SELECT id_habilidade FROM Cura WHERE nome = 'Pausa para o Café'));
```

---

## Inserções na tabela **habilidade_estudante**

```sql
-- Populando tabela 'habilidade_estudante'
INSERT INTO habilidade_estudante (id_estudante, id_habilidade) VALUES
(1, (SELECT id_habilidade FROM Ataque WHERE nome = 'Ataque Básico')),
(1, (SELECT id_habilidade FROM Defesa WHERE nome = 'Corrida Rápida')),
(1, (SELECT id_habilidade FROM Cura WHERE nome = 'Curativo Simples')),
(2, (SELECT id_habilidade FROM Ataque WHERE nome = 'Ataque Básico')),
(2, (SELECT id_habilidade FROM Defesa WHERE nome = 'Corrida Rápida')),
(2, (SELECT id_habilidade FROM Cura WHERE nome = 'Curativo Simples')),
(3, (SELECT id_habilidade FROM Ataque WHERE nome = 'Ataque Básico')),
(3, (SELECT id_habilidade FROM Defesa WHERE nome = 'Corrida Rápida')),
(3, (SELECT id_habilidade FROM Cura WHERE nome = 'Curativo Simples')),
(4, (SELECT id_habilidade FROM Ataque WHERE nome = 'Ataque Básico')),
(4, (SELECT id_habilidade FROM Defesa WHERE nome = 'Corrida Rápida')),
(4, (SELECT id_habilidade FROM Cura WHERE nome = 'Curativo Simples')),
(5, (SELECT id_habilidade FROM Ataque WHERE nome = 'Ataque Básico')),
(5, (SELECT id_habilidade FROM Defesa WHERE nome = 'Corrida Rápida')),
(5, (SELECT id_habilidade FROM Cura WHERE nome = 'Curativo Simples'));
```

---

## Inserções na tabela **habilidade_loja** – bloco DO

```sql
-- Populando tabela 'habilidade_loja'
DO $$
DECLARE
    shop_sala_id INT;
    habilidade_id INT;
BEGIN
    FOR shop_sala_id IN (SELECT id_sala FROM sala_comum WHERE tem_loja = TRUE) LOOP
        FOR habilidade_id IN (SELECT id_habilidade FROM tipoHabilidade ORDER BY random() LIMIT 5) LOOP
            INSERT INTO habilidade_loja (id_loja, id_habilidade) VALUES (shop_sala_id, habilidade_id);
        END LOOP;
    END LOOP;
END $$;
```

---

## Inserções na tabela **instancia_de_item** – bloco DO + extras

```sql
-- Populando tabela 'instancia_de_item'
DO $$
DECLARE
    i INT;
    instance_count INT := 10;
    random_item_id INT;
    random_sala_id INT;
    random_estudante_id INT;
    v_item_tipo CHAR(10);
    equipado_val BOOLEAN;
BEGIN
    FOR i IN 1..instance_count LOOP
        SELECT id_item, item_tipo INTO random_item_id, v_item_tipo
        FROM tipo_item
        ORDER BY random()
        LIMIT 1;

        IF v_item_tipo = 'Equipável' THEN
            equipado_val := FALSE;
        ELSE
            equipado_val := NULL;
        END IF;

        SELECT id_sala INTO random_sala_id FROM sala_comum ORDER BY random() LIMIT 1;
        SELECT id_estudante INTO random_estudante_id FROM estudante ORDER BY random() LIMIT 1;

        IF random() > 0.5 THEN
            INSERT INTO instancia_de_item (id_item, id_sala, id_estudante, equipado)
            VALUES (random_item_id, random_sala_id, NULL, equipado_val);
        ELSE
            INSERT INTO instancia_de_item (id_item, id_sala, id_estudante, equipado)
            VALUES (random_item_id, NULL, random_estudante_id, equipado_val);
        END IF;
    END LOOP;
END $$;

INSERT INTO instancia_de_item (id_item, id_sala, id_estudante, equipado) VALUES 
        (11, NULL, 4, FALSE),
        (12, NULL, 4, TRUE);
```




### Histórico de Versões

| Versão | Data       | Descrição                           | Autor              |
|--------|------------|-------------------------------------|--------------------|
| 1.0    | 12/06/2025 | Carga inicial de dados no sistema   | Rodrigo Amaral     |
| 2.0    | 07/07/2025 | Edição da carga inicial de dados no sistema para a versão final   | Isaque Camargos     |