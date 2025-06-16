# DML

DML (Data Manipulation Language) é a parte da linguagem SQL usada para inserir, atualizar, deletar e manipular dados dentro das tabelas de um banco de dados.

Neste contexto, o script `DML.sql` foi utilizado para popular o banco de dados com dados iniciais, simulando um ambiente completo de um RPG acadêmico baseado em temas universitários da Universidade de Brasília (UnB);

## Operações realizadas

### Inserção de temas

```sql
INSERT INTO tema (nome) VALUES
('Matemática'),
('Programação'),
('Engenharias'),
('Humanidades'),
('Gerais');
```
Cada tema representa uma área do conhecimento presente no RPG.

---

### Inserção de habilidades

```sql
INSERT INTO habilidades (nome, tipo_habilidade, nivel, coolDown, id_tema) VALUES
-- Matemática (id_tema = 1)
('Equação Quadrática', 'A', 5, 2, 1),
('Teorema de Pitágoras', 'A', 8, 3, 1),
('Cálculo Integral', 'A', 15, 5, 1),
('Defesa Numérica', 'D', 7, 2, 1),
('Revisão de Conceitos', 'C', 4, 3, 1),
-- Programação (id_tema = 2)
('Bug Report', 'A', 6, 2, 2),
('Debug Rápido', 'A', 10, 3, 2),
('Zero Division', 'A', 18, 6, 2),
('Firewall Pessoal', 'D', 9, 2, 2),
('Stack Overflow', 'C', 5, 3, 2),
-- Engenharias (id_tema = 3)
('Desenho Técnico', 'A', 7, 2, 3),
('Análise Estrutural', 'A', 12, 4, 3),
('Falha de Projeto', 'A', 17, 5, 3),
('Material Resistente', 'D', 8, 2, 3),
('Reparo de Circuito', 'C', 6, 3, 3),
-- Humanidades (id_tema = 4)
('Retórica Persuasiva', 'A', 5, 2, 4),
('Crítica Social', 'A', 9, 3, 4),
('Argumento Irrefutável', 'A', 16, 5, 4),
('Escudo Cultural', 'D', 7, 2, 4),
('Sessão de Terapia', 'C', 4, 3, 4),
-- Gerais (id_tema = 5)
('Ataque Básico', 'A', 1, 1, 5),
('Corrida Rápida', 'D', 2, 1, 5),
('Curativo Simples', 'C', 1, 1, 5),
('Estudo Avançado', 'A', 10, 4, 5),
('Pausa para o Café', 'C', 7, 2, 5),
('Concentração Total', 'D', 11, 3, 5);
```
As habilidades são divididas por tipo:
- `A` = Ataque
- `D` = Defesa
- `C` = Cura

---

### Inserção de criaturas

```sql
-- Monstros Simples (Nível <= 15) - Relacionados aos temas 
-- Programação
INSERT INTO criatura (nivel, vida_max, tipo_criatura, nome, descricao) VALUES
(3, 30, 'Monstro Simples', 'Erro de Sintaxe', 'Um pequeno erro que atrapalha o código.'),
(9, 70, 'Monstro Simples', 'Loop Infinito', 'Um programa que nunca termina.'),  
-- Matemática
(5, 45, 'Monstro Simples', 'Derivada Confusa', 'Uma função matemática que parece não ter fim.'), 
(11, 85, 'Monstro Simples', 'Paradoxo Lógico', 'Um problema que desafia a razão.'),
-- Humanidades
(7, 60, 'Monstro Simples', 'Plágio Descarado', 'Uma ameaça à originalidade acadêmica.'),
(13, 100, 'Monstro Simples', 'Teoria da Conspiração', 'Uma narrativa sem evidências, mas persistente.'),
-- Engenharias 
(4, 35, 'Monstro Simples', 'Fio Solto', 'Um defeito simples em uma instalação elétrica.'),
(10, 75, 'Monstro Simples', 'Solda Fria', 'Uma conexão mal feita que causa instabilidade.'), 
-- Gerais
(6, 50, 'Monstro Simples', 'Preguiça Matinal', 'A força que impede o estudante de levantar.'),
(8, 65, 'Monstro Simples', 'Distração Coletiva', 'O inimigo de toda sessão de estudos.')

-- Bosses (Nível = 20) 
-- Boss de Matemática
(20, 200, 'Boss', 'Professor Álgebra', 'Um mestre implacável da matemática abstrata.'), 
-- Boss de Programação
(20, 220, 'Boss', 'O Último Compilador', 'O guardião supremo da lógica de programação.'), 
-- Boss de Humanidades
(20, 210, 'Boss', 'A Burocracia Impiedosa', 'Um sistema complexo que desafia a paciência de todos.'), 
-- Boss de Engenharias
(20, 230, 'Boss', 'O Gigante de Concreto', 'Uma estrutura colossal que testa a engenharia.'), 
-- Boss Gerais
(20, 190, 'Boss', 'A Crise Existencial', 'A dúvida que assola todo estudante na reta final.'); 
```
Inclui monstros simples (nível ≤ 15) e bosses (nível = 20).

---

### Inserção de campus e setores

```sql
INSERT INTO campus (nome, descricao) VALUES
('UnB Campus Gama', 'O coração da jornada acadêmica do RPG-FGA.');

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
Os setores são interligados de forma circular com `id_proxSetor` e `id_prevSetor`.

---

### Geração de salas comuns com lojas e dungeons

```sql
DO $$
DECLARE
    i INT;
    sector_id INT;
    room_count INT := 10;
    shop_assigned BOOLEAN;
    dungeon_assigned BOOLEAN;
    prev_room_id INT;
BEGIN

    -- Verifica se há setores disponíveis
    IF NOT EXISTS (SELECT 1 FROM setor) THEN
        RAISE EXCEPTION 'Tabela setor está vazia. Verifique as inserções anteriores.';
    END IF;

    FOR sector_id IN 1..6 LOOP
        shop_assigned := FALSE;
        dungeon_assigned := FALSE;
        prev_room_id := NULL; -- Reinicia para cada setor

        FOR i IN 1..room_count LOOP
            DECLARE
                room_name VARCHAR(100);
                room_desc VARCHAR(255);
                has_shop BOOLEAN := FALSE;
                has_dungeon BOOLEAN := FALSE;
                current_room_id INT;
            BEGIN
                -- Garante pelo menos uma loja e uma dungeon por setor 
                IF NOT shop_assigned AND i = 1 THEN
                    has_shop := TRUE;
                    shop_assigned := TRUE;
                ELSIF NOT dungeon_assigned AND i = 2 THEN
                    has_dungeon := TRUE;
                    dungeon_assigned := TRUE;
                ELSE
                    -- Atribui lojas e dungeons aleatoriamente para as salas restantes
                    has_shop := (random() < 0.3);
                    has_dungeon := (random() < 0.2);
                END IF;

                CASE sector_id
                    WHEN 1 THEN -- UED
                        room_name := 'Laboratório de Redes ' || i;
                        room_desc := 'Um laboratório de informática focado em redes.';
                    WHEN 2 THEN -- Containers
                        room_name := 'Laboratório de IoT ' || i;
                        room_desc := 'Um laboratório modular para projetos de Internet das Coisas.';
                    WHEN 3 THEN -- UAC
                        room_name := 'Sala S-' || i;
                        room_desc := 'Uma sala de aula padrão do UAC.';
                    WHEN 4 THEN -- Refeitório Universitário
                        room_name := 'Mesa ' || i;
                        room_desc := 'Uma mesa no refeitório, ideal para uma refeição rápida.';
                    WHEN 5 THEN -- Estacionamento
                        room_name := 'Lote E-' || i;
                        room_desc := 'Um dos lotes do estacionamento do campus.';
                    WHEN 6 THEN -- LDTEA
                        room_name := 'Laboratório de Protótipos ' || i;
                        room_desc := 'Um laboratório para criação de protótipos e maquetes.';
                    ELSE
                        room_name := 'Sala Genérica ' || i;
                        room_desc := 'Uma sala comum qualquer.';
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
        -- Liga a última sala à primeira sala no ciclo para cada setor
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
Cada setor possui 10 salas, com pelo menos uma loja e uma dungeon.

---

### Inserção de estudantes e suas afinidades

```sql
INSERT INTO estudante (id_sala, nome, vida, estresse, total_dinheiro) VALUES
((SELECT id_sala FROM sala_comum WHERE id_setor = 1 ORDER BY id_sala LIMIT 1), 'Alice Dev', 20, 20, 10),
((SELECT id_sala FROM sala_comum WHERE id_setor = 2 ORDER BY id_sala LIMIT 1), 'Léo Eng', 20, 20, 10),
((SELECT id_sala FROM sala_comum WHERE id_setor = 3 ORDER BY id_sala LIMIT 1), 'Carlos Mat', 20, 20, 10),
((SELECT id_sala FROM sala_comum WHERE id_setor = 4 ORDER BY id_sala LIMIT 1), 'Diana Hum', 20, 20, 10),
((SELECT id_sala FROM sala_comum WHERE id_setor = 5 ORDER BY id_sala LIMIT 1), 'Eduardo G', 20, 20, 10);
 
INSERT INTO afinidade (id_estudante, id_tema, xp_atual, nivel_atual) VALUES
(1, 1, 0, 1), (1, 2, 0, 1), (1, 3, 0, 1), (1, 4, 0, 1), (1, 5, 0, 1),
(2, 1, 0, 1), (2, 2, 0, 1), (2, 3, 0, 1), (2, 4, 0, 1), (2, 5, 0, 1),
(3, 1, 0, 1), (3, 2, 0, 1), (3, 3, 0, 1), (3, 4, 0, 1), (3, 5, 0, 1),
(4, 1, 0, 1), (4, 2, 0, 1), (4, 3, 0, 1), (4, 4, 0, 1), (4, 5, 0, 1),
(5, 1, 0, 1), (5, 2, 0, 1), (5, 3, 0, 1), (5, 4, 0, 1), (5, 5, 0, 1);
```
Cada estudante começa com afinidade nível 1 e 0 XP para cada tema.

---

### Inserção de itens
```sql

INSERT INTO reliquia (tipo) VALUES
('Cálculo Infinito'), -- Matemática
('Código Fonte Universal'), -- Programação
('Projeto Mestre'), -- Engenharias
('Sabedoria Ancestral'), -- Humanidades
('Conhecimento Geral Abrangente'); -- Gerais

INSERT INTO item (nome, descricao, item_tipo) VALUES
-- Consumíveis 
('Café Expresso', 'Recupera um pouco de estresse e te dá energia.', 'Consumível'),
('Barra de Cereal', 'Um lanche rápido para restaurar a vitalidade.', 'Consumível'),
('Comprimido Analgésico', 'Alivia dores de cabeça e ajuda a focar.', 'Consumível'),
('Guaraná Natural', 'Aumenta sua vida por um curto período.', 'Consumível'),
('Chocolate Acadêmico', 'Melhora o humor e a concentração.', 'Consumível'),
-- Equipáveis (Não Consumíveis) 
('Óculos de Leitura Avançada', 'Aumenta sua vida máxima permanentemente.', 'Equipavel'),
('Mochila de Estudo', 'Permite carregar mais itens.', 'Equipavel'),
('Tênis Confortável', 'Aumenta sua capacidade de fuga em combate.', 'Equipavel'),
-- Monetário 
('Moeda Acadêmica', 'A moeda corrente do campus.', 'Monetario'),
('Ficha de RU', 'Pode ser trocada por refeições.', 'Monetario');

-- Populando tabela 'consumivel'   
INSERT INTO consumivel (id_item, efeito, preco) VALUES
((SELECT id_item FROM item WHERE nome = 'Café Expresso'), 5.0, 3.0),
((SELECT id_item FROM item WHERE nome = 'Barra de Cereal'), 10.0, 5.0),
((SELECT id_item FROM item WHERE nome = 'Comprimido Analgésico'), 7.0, 4.0),
((SELECT id_item FROM item WHERE nome = 'Guaraná Natural'), 15.0, 8.0),
((SELECT id_item FROM item WHERE nome = 'Chocolate Acadêmico'), 12.0, 6.0);

-- Populando tabela 'equipavel'   
INSERT INTO equipavel (id_item, efeito, preco, equipado) VALUES
((SELECT id_item FROM item WHERE nome = 'Óculos de Leitura Avançada'), 10, 50, FALSE),
((SELECT id_item FROM item WHERE nome = 'Mochila de Estudo'), 5, 30, FALSE),
((SELECT id_item FROM item WHERE item.nome = 'Tênis Confortável'), 2, 40, FALSE);

-- Populando tabela 'monetario'   
INSERT INTO monetario (id_item, valor) VALUES
((SELECT id_item FROM item WHERE nome = 'Moeda Acadêmica'), 1),
((SELECT id_item FROM item WHERE nome = 'Ficha de RU'), 5);
```
---

### Inserção de lojas

```sql
INSERT INTO loja (nome) VALUES
('Loja UED Materiais'),
('Cantina Containers'),
('Livraria UAC'),
('Empório RU'),
('Loja de Conveniência Estacionamento'),
('Papelaria LDTEA');

-- Populando tabela 'loja_item'   (Apenas itens consumíveis nas lojas) 
DO $$
DECLARE
    shop_sala_id INT;
    consumivel_id INT;
BEGIN
    FOR shop_sala_id IN (SELECT id_sala FROM sala_comum WHERE tem_loja = TRUE) LOOP
        -- Adiciona uma seleção aleatória de itens consumíveis para cada loja 
        FOR consumivel_id IN (SELECT id_item FROM consumivel ORDER BY random() LIMIT 3) LOOP
            INSERT INTO loja_item (id_sala, id_item) VALUES (shop_sala_id, consumivel_id);
        END LOOP;
    END LOOP;
END $$;
```
Cada loja recebe itens consumíveis aleatórios.

---

### Inserção de habilidades de criaturas e de estudantes

```sql
INSERT INTO habilidade_criatura (id_criatura, id_habilidade) VALUES
-- Erro de Sintaxe (Programação)
((SELECT id_criatura FROM criatura WHERE nome = 'Erro de Sintaxe'), (SELECT id_habilidade FROM habilidades WHERE nome = 'Bug Report')),
((SELECT id_criatura FROM criatura WHERE nome = 'Erro de Sintaxe'), (SELECT id_habilidade FROM habilidades WHERE nome = 'Ataque Básico')),
-- Derivada Confusa (Matemática)
((SELECT id_criatura FROM criatura WHERE nome = 'Derivada Confusa'), (SELECT id_habilidade FROM habilidades WHERE nome = 'Equação Quadrática')),
((SELECT id_criatura FROM criatura WHERE criatura.nome = 'Derivada Confusa'), (SELECT id_habilidade FROM habilidades WHERE nome = 'Defesa Numérica')),
-- Plágio Descarado (Humanidades)
((SELECT id_criatura FROM criatura WHERE nome = 'Plágio Descarado'), (SELECT id_habilidade FROM habilidades WHERE nome = 'Retórica Persuasiva')),
((SELECT id_criatura FROM criatura WHERE nome = 'Plágio Descarado'), (SELECT id_habilidade FROM habilidades WHERE nome = 'Crítica Social')),
-- Fio Solto (Engenharias)
((SELECT id_criatura FROM criatura WHERE nome = 'Fio Solto'), (SELECT id_habilidade FROM habilidades WHERE nome = 'Desenho Técnico')),
((SELECT id_criatura FROM criatura WHERE nome = 'Fio Solto'), (SELECT id_habilidade FROM habilidades WHERE nome = 'Material Resistente')),
-- Preguiça Matinal (Gerais)
((SELECT id_criatura FROM criatura WHERE nome = 'Preguiça Matinal'), (SELECT id_habilidade FROM habilidades WHERE nome = 'Ataque Básico')),
((SELECT id_criatura FROM criatura WHERE nome = 'Preguiça Matinal'), (SELECT id_habilidade FROM habilidades WHERE nome = 'Pausa para o Café')),
-- Loop Infinito (Programação)
((SELECT id_criatura FROM criatura WHERE nome = 'Loop Infinito'), (SELECT id_habilidade FROM habilidades WHERE nome = 'Debug Rápido')),
((SELECT id_criatura FROM criatura WHERE nome = 'Loop Infinito'), (SELECT id_habilidade FROM habilidades WHERE nome = 'Zero Division')),
-- Paradoxo Lógico (Matemática)
((SELECT id_criatura FROM criatura WHERE nome = 'Paradoxo Lógico'), (SELECT id_habilidade FROM habilidades WHERE nome = 'Teorema de Pitágoras')),
((SELECT id_criatura FROM criatura WHERE nome = 'Paradoxo Lógico'), (SELECT id_habilidade FROM habilidades WHERE nome = 'Cálculo Integral')),
-- Teoria da Conspiração (Humanidades)
((SELECT id_criatura FROM criatura WHERE nome = 'Teoria da Conspiração'), (SELECT id_habilidade FROM habilidades WHERE nome = 'Argumento Irrefutável')),
((SELECT id_criatura FROM criatura WHERE nome = 'Teoria da Conspiração'), (SELECT id_habilidade FROM habilidades WHERE nome = 'Escudo Cultural')),
-- Solda Fria (Engenharias)
((SELECT id_criatura FROM criatura WHERE nome = 'Solda Fria'), (SELECT id_habilidade FROM habilidades WHERE nome = 'Análise Estrutural')),
((SELECT id_criatura FROM criatura WHERE nome = 'Solda Fria'), (SELECT id_habilidade FROM habilidades WHERE nome = 'Falha de Projeto')),
-- Distração Coletiva (Gerais)
((SELECT id_criatura FROM criatura WHERE nome = 'Distração Coletiva'), (SELECT id_habilidade FROM habilidades WHERE nome = 'Estudo Avançado')),
((SELECT id_criatura FROM criatura WHERE nome = 'Distração Coletiva'), (SELECT id_habilidade FROM habilidades WHERE nome = 'Concentração Total')),

-- Populando tabela 'habilidade_estudante'   
INSERT INTO habilidade_estudante (id_estudante, id_habilidade) VALUES
(1, (SELECT id_habilidade FROM habilidades WHERE nome = 'Ataque Básico')),
(1, (SELECT id_habilidade FROM habilidades WHERE nome = 'Corrida Rápida')),
(1, (SELECT id_habilidade FROM habilidades WHERE nome = 'Curativo Simples')),
(2, (SELECT id_habilidade FROM habilidades WHERE nome = 'Ataque Básico')),
(2, (SELECT id_habilidade FROM habilidades WHERE nome = 'Corrida Rápida')),
(2, (SELECT id_habilidade FROM habilidades WHERE nome = 'Curativo Simples')),
(3, (SELECT id_habilidade FROM habilidades WHERE nome = 'Ataque Básico')),
(3, (SELECT id_habilidade FROM habilidades WHERE nome = 'Corrida Rápida')),
(3, (SELECT id_habilidade FROM habilidades WHERE nome = 'Curativo Simples')),
(4, (SELECT id_habilidade FROM habilidades WHERE nome = 'Ataque Básico')),
(4, (SELECT id_habilidade FROM habilidades WHERE nome = 'Corrida Rápida')),
(4, (SELECT id_habilidade FROM habilidades WHERE nome = 'Curativo Simples')),
(5, (SELECT id_habilidade FROM habilidades WHERE nome = 'Ataque Básico')),
(5, (SELECT id_habilidade FROM habilidades WHERE nome = 'Corrida Rápida')),
(5, (SELECT id_habilidade FROM habilidades WHERE nome = 'Curativo Simples'));
```
Cada criatura recebe habilidades compatíveis com seu tema. 
Estudantes começam com habilidades básicas como "Ataque Básico", "Curativo Simples" e "Corrida Rápida".

---

### Inserção de dungeons e seus bosses

```sql
INSERT INTO dungeon_academica (nome, descricao, id_tema) VALUES
('Matemática Quântica', 'Uma dungeon onde os números se comportam de maneira imprevisível.', 1),
('Labirinto de Códigos', 'Um ambiente complexo cheio de algoritmos e funções enigmáticas.', 2),
('Fundição de Ideias', 'Um lugar onde projetos complexos ganham vida e testam os limites da engenharia.', 3),
('Debate Filosófico', 'Um salão onde as ideias se chocam e a retórica é a principal arma.', 4),
('O Grande Auditório', 'Um local de conhecimento vasto e diversificado, onde tudo pode ser aprendido.', 5);

-- Populando tabela 'boss'   
-- Ligando cada boss a uma relíquia única.
INSERT INTO boss (id_boss, id_reliquia) VALUES
(
    (SELECT id_criatura FROM criatura WHERE nome = 'Professor Álgebra'),
    (SELECT id_reliquia FROM reliquia WHERE tipo = 'Cálculo Infinito')
),
(
    (SELECT id_criatura FROM criatura WHERE nome = 'O Último Compilador'),
    (SELECT id_reliquia FROM reliquia WHERE tipo = 'Código Fonte Universal')
),
(
    (SELECT id_criatura FROM criatura WHERE nome = 'O Gigante de Concreto'),
    (SELECT id_reliquia FROM reliquia WHERE tipo = 'Projeto Mestre')
),
(
    (SELECT id_criatura FROM criatura WHERE nome = 'A Burocracia Impiedosa'),
    (SELECT id_reliquia FROM reliquia WHERE tipo = 'Sabedoria Ancestral')
),
(
    (SELECT id_criatura FROM criatura WHERE nome = 'A Crise Existencial'),
    (SELECT id_reliquia FROM reliquia WHERE tipo = 'Conhecimento Geral Abrangente')
);
```
Cada dungeon é vinculada a um tema e tem um boss, que por sua vez carrega uma relíquia.

---

### Inserção na tabela habilidade_loja  

```sql
-- Distribuindo aleatoriamente algumas habilidades entre as lojas 
DO $$
DECLARE
    loja_id INT;
    habilidade_id INT;
BEGIN
    FOR loja_id IN (SELECT id_loja FROM loja) LOOP
        -- Seleciona um conjunto aleatório de habilidades para cada loja 
        FOR habilidade_id IN (SELECT id_habilidade FROM habilidades ORDER BY random() LIMIT 5) LOOP
            INSERT INTO habilidade_loja (id_loja, id_habilidade) VALUES (loja_id, habilidade_id);
        END LOOP;
    END LOOP;
END $$;
```

### Inserção na tabela 'instancia_de_item' 

```sql
-- 10 instâncias distribuídas aleatoriamente entre salas e estudantes
DO $$
DECLARE
    instance_count INT := 10;
    random_item_id INT;
    random_sala_id INT;
    random_estudante_id INT;
BEGIN
    IF NOT EXISTS (SELECT 1 FROM sala_comum) THEN
        RAISE EXCEPTION 'Tabela sala_comum está vazia. Verifique as inserções anteriores.';
    END IF;
    IF NOT EXISTS (SELECT 1 FROM estudante) THEN
        RAISE EXCEPTION 'Tabela estudante está vazia. Verifique as inserções anteriores.';
    END IF;

    FOR i IN 1..instance_count LOOP
        SELECT id_item INTO random_item_id FROM item ORDER BY random() LIMIT 1;
        SELECT id_sala INTO random_sala_id FROM sala_comum ORDER BY random() LIMIT 1;
        SELECT id_estudante INTO random_estudante_id FROM estudante ORDER BY random() LIMIT 1;

        INSERT INTO instancia_de_item (id_item, id_sala, id_estudante) VALUES
        (random_item_id, random_sala_id, random_estudante_id);
    END LOOP;
END $$;
```

### Inserção de habilidades ofensivas, defensivas e de cura

```sql
INSERT INTO Ataque (id_habilidade, danoCausado, porcentagemAcerto) VALUES
((SELECT id_habilidade FROM habilidades WHERE nome = 'Equação Quadrática'), 15, 0.9),
((SELECT id_habilidade FROM habilidades WHERE nome = 'Teorema de Pitágoras'), 20, 0.95),
((SELECT id_habilidade FROM habilidades WHERE nome = 'Cálculo Integral'), 30, 0.85),
((SELECT id_habilidade FROM habilidades WHERE nome = 'Bug Report'), 16, 0.9),
((SELECT id_habilidade FROM habilidades WHERE nome = 'Debug Rápido'), 22, 0.92),
((SELECT id_habilidade FROM habilidades WHERE nome = 'Zero Division'), 35, 0.8),
((SELECT id_habilidade FROM habilidades WHERE nome = 'Desenho Técnico'), 18, 0.88),
((SELECT id_habilidade FROM habilidades WHERE nome = 'Análise Estrutural'), 25, 0.9),
((SELECT id_habilidade FROM habilidades WHERE nome = 'Falha de Projeto'), 32, 0.85),
((SELECT id_habilidade FROM habilidades WHERE nome = 'Retórica Persuasiva'), 14, 0.9),
((SELECT id_habilidade FROM habilidades WHERE nome = 'Crítica Social'), 19, 0.92),
((SELECT id_habilidade FROM habilidades WHERE nome = 'Argumento Irrefutável'), 28, 0.87),
((SELECT id_habilidade FROM habilidades WHERE nome = 'Ataque Básico'), 8, 0.98),
((SELECT id_habilidade FROM habilidades WHERE nome = 'Estudo Avançado'), 20, 0.89);

-- Populando tabela 'Cura'
INSERT INTO Cura (id_habilidade, vidaRecuperada) VALUES
((SELECT id_habilidade FROM habilidades WHERE nome = 'Revisão de Conceitos'), 10),
((SELECT id_habilidade FROM habilidades WHERE nome = 'Stack Overflow'), 12),
((SELECT id_habilidade FROM habilidades WHERE nome = 'Reparo de Circuito'), 11),
((SELECT id_habilidade FROM habilidades WHERE nome = 'Sessão de Terapia'), 9),
((SELECT id_habilidade FROM habilidades WHERE nome = 'Curativo Simples'), 5),
((SELECT id_habilidade FROM habilidades WHERE nome = 'Pausa para o Café'), 15);

-- Populando tabela 'Defesa'
INSERT INTO Defesa (id_habilidade, danoMitigado) VALUES
((SELECT id_habilidade FROM habilidades WHERE nome = 'Defesa Numérica'), 10),
((SELECT id_habilidade FROM habilidades WHERE nome = 'Firewall Pessoal'), 13),
((SELECT id_habilidade FROM habilidades WHERE nome = 'Material Resistente'), 11),
((SELECT id_habilidade FROM habilidades WHERE nome = 'Escudo Cultural'), 9),
((SELECT id_habilidade FROM habilidades WHERE nome = 'Corrida Rápida'), 7),
((SELECT id_habilidade FROM habilidades WHERE nome = 'Concentração Total'), 14);
```
Define as propriedades específicas das habilidades por tipo (ex: dano causado, mitigado ou vida recuperada).

---

### Histórico de Versões

| Versão | Data       | Descrição                           | Autor              |
|--------|------------|-------------------------------------|--------------------|
| 1.0    | 12/06/2025 | Carga inicial de dados no sistema   | Rodrigo Amaral     |