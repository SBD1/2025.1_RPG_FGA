-- --------------------------------------------------------------------------------------
-- Data Criacao ...........: 12/06/2025                                                --
-- Autor(es) ..............: Rodrigo Amaral                                            --
-- Versao ..............: 2.0                                                          --
-- Banco de Dados .........: PostgreSQL                                                --
-- Descricao .........: Carga de todas as tabelas do banco de dados.                   --
-- --------------------------------------------------------------------------------------
-- | Atualizacao : 12/06/2025 | Autor(es): Rodrigo Amaral                       |      --
--                            | Descricao: Inclusão das linhas de INSERT INTO   |      --
-- | Atualizacao : 05/07/2025 | Autor(es): Rodrigo Amaral                       |      --
--                            | Descricao: Atualização de INSERT INTO           |      --
-- --------------------------------------------------------------------------------------

-- DML para o novo esquema (com correções para boss, monstro_simples, instancias e habilidades)

-- Populating 'tema' table
INSERT INTO tema (nome) VALUES
('Matemática'),
('Programação'),
('Engenharias'),
('Humanidades'),
('Gerais');

-- Populating 'tipoHabilidade' table
INSERT INTO tipoHabilidade (tipo_habilidade) VALUES
('ataque'),
('cura'),
('defesa');

-- Populating 'tipo_criatura' table
INSERT INTO tipo_criatura (tipo_criatura) VALUES
('Monstro'),
('Boss');

-- Populating 'tipo_item' table (Apenas uma entrada para cada tipo)
INSERT INTO tipo_item (item_tipo) VALUES
('Consumível'),
('Equipável'),
('Monetário'),
('Relíquia');

-- Populating 'campus' table
INSERT INTO campus (nome, descricao) VALUES
('UnB Campus Gama', 'O coração da jornada acadêmica do RPG-FGA.                                                                                                                                                                                                                                           ');

-- Populating 'setor' table
INSERT INTO setor (id_campus, nome, descricao) VALUES
(1, 'UED       ', 'Unidade de Ensino à Distância, com laboratórios e salas de professores.                                                                                                                                                                                                 '),
(1, 'Containers', 'Setor de laboratórios específicos, construídos em containers.                                                                                                                                                                                                       '),
(1, 'UAC       ', 'Unidade Acadêmica Central, com salas numeradas.                                                                                                                                                                                                                    '),
(1, 'Refeitório', 'Local de alimentação e descanso para os estudantes.                                                                                                                                                                                                                '),
(1, 'Estacionam', 'Área externa para veículos e um espaço de lazer.                                                                                                                                                                                                                  '),
(1, 'LDTEA     ', 'Laboratório de Desenho Técnico e Expressão Artística.                                                                                                                                                                                                             ');

UPDATE setor SET id_proxSetor = 2, id_prevSetor = 6 WHERE id_setor = 1;
UPDATE setor SET id_proxSetor = 3, id_prevSetor = 1 WHERE id_setor = 2;
UPDATE setor SET id_proxSetor = 4, id_prevSetor = 2 WHERE id_setor = 3;
UPDATE setor SET id_proxSetor = 5, id_prevSetor = 3 WHERE id_setor = 4;
UPDATE setor SET id_proxSetor = 6, id_prevSetor = 4 WHERE id_setor = 5;
UPDATE setor SET id_proxSetor = 1, id_prevSetor = 5 WHERE id_setor = 6;

-- Populating 'sala_comum' table
DO $$
DECLARE
    i INT;
    sector_id INT;
    room_count INT := 10;
    shop_assigned BOOLEAN;
    dungeon_assigned BOOLEAN;
    prev_room_id INT;
    current_room_id INT;
    first_room_in_sector_id INT;
BEGIN
    FOR sector_id IN 1..6 LOOP
        shop_assigned := FALSE;
        dungeon_assigned := FALSE;
        prev_room_id := NULL;
        first_room_in_sector_id := NULL;

        FOR i IN 1..room_count LOOP
            DECLARE
                room_name_val CHAR(100);
                room_desc_val CHAR(255);
                has_shop_val BOOLEAN := FALSE;
                has_dungeon_val BOOLEAN := FALSE;
            BEGIN
                IF NOT shop_assigned AND i = 1 THEN
                    has_shop_val := TRUE;
                    shop_assigned := TRUE;
                ELSIF NOT dungeon_assigned AND i = 2 THEN
                    has_dungeon_val := TRUE;
                    dungeon_assigned := TRUE;
                ELSE
                    has_shop_val := (random() < 0.3);
                    has_dungeon_val := (random() < 0.2);
                END IF;

                CASE sector_id
                    WHEN 1 THEN room_name_val := LPAD('Laboratório de Redes ' || i, 100, ' '); room_desc_val := LPAD('Um laboratório de informática focado em redes.', 255, ' ');
                    WHEN 2 THEN room_name_val := LPAD('Laboratório de IoT ' || i, 100, ' '); room_desc_val := LPAD('Um laboratório modular para projetos de Internet das Coisas.', 255, ' ');
                    WHEN 3 THEN room_name_val := LPAD('Sala SX' || i, 100, ' '); room_desc_val := LPAD('Uma sala de aula padrão do UAC.', 255, ' ');
                    WHEN 4 THEN room_name_val := LPAD('Mesa ' || i, 100, ' '); room_desc_val := LPAD('Uma mesa no refeitório, ideal para uma refeição rápida.', 255, ' ');
                    WHEN 5 THEN room_name_val := LPAD('Lote E' || i, 100, ' '); room_desc_val := LPAD('Um dos lotes do estacionamento do campus.', 255, ' ');
                    WHEN 6 THEN room_name_val := LPAD('Laboratório de Protótipos ' || i, 100, ' '); room_desc_val := LPAD('Um laboratório para criação de protótipos e maquetes.', 255, ' ');
                    ELSE room_name_val := LPAD('Sala Genérica ' || i, 100, ' '); room_desc_val := LPAD('Uma sala comum qualquer.', 255, ' ');
                END CASE;

                INSERT INTO sala_comum (id_setor, id_prevSala, nome, descricao, tem_loja, tem_dungeon) VALUES
                (sector_id, prev_room_id, room_name_val, room_desc_val, has_shop_val, has_dungeon_val)
                RETURNING id_sala INTO current_room_id;

                IF first_room_in_sector_id IS NULL THEN first_room_in_sector_id := current_room_id; END IF;
                IF prev_room_id IS NOT NULL THEN UPDATE sala_comum SET id_proxSala = current_room_id WHERE id_sala = prev_room_id AND id_setor = sector_id; END IF;
                prev_room_id := current_room_id;
            END;
        END LOOP;
        IF prev_room_id IS NOT NULL AND first_room_in_sector_id IS NOT NULL THEN
            UPDATE sala_comum SET id_proxSala = first_room_in_sector_id WHERE id_sala = prev_room_id AND id_setor = sector_id;
            UPDATE sala_comum SET id_prevSala = prev_room_id WHERE id_sala = first_room_in_sector_id AND id_setor = sector_id;
        END IF;
    END LOOP;
END $$;

-- Populating 'estudante' table
INSERT INTO estudante (id_sala, nome, vida, estresse, total_dinheiro) VALUES
((SELECT id_sala FROM sala_comum WHERE id_setor = 1 ORDER BY id_sala ASC LIMIT 1), 'Alice Dev                                                             ', 20, 20, 10),
((SELECT id_sala FROM sala_comum WHERE id_setor = 2 ORDER BY id_sala ASC LIMIT 1), 'Bob Eng                                                               ', 20, 20, 10),
((SELECT id_sala FROM sala_comum WHERE id_setor = 3 ORDER BY id_sala ASC LIMIT 1), 'Carlos Mat                                                            ', 20, 20, 10),
((SELECT id_sala FROM sala_comum WHERE id_setor = 4 ORDER BY id_sala ASC LIMIT 1), 'Diana Hum                                                             ', 20, 20, 10),
((SELECT id_sala FROM sala_comum WHERE id_setor = 5 ORDER BY id_sala ASC LIMIT 1), 'Eduardo G                                                             ', 20, 20, 10);

-- Populating 'afinidade' table
INSERT INTO afinidade (id_estudante, id_tema, xp_atual, nivel_atual) VALUES
(1, 1, 0, 1), (1, 2, 0, 1), (1, 3, 0, 1), (1, 4, 0, 1), (1, 5, 0, 1),
(2, 1, 0, 1), (2, 2, 0, 1), (2, 3, 0, 1), (2, 4, 0, 1), (2, 5, 0, 1),
(3, 1, 0, 1), (3, 2, 0, 1), (3, 3, 0, 1), (3, 4, 0, 1), (3, 5, 0, 1),
(4, 1, 0, 1), (4, 2, 0, 1), (4, 3, 0, 1), (4, 4, 0, 1), (4, 5, 0, 1),
(5, 1, 0, 1), (5, 2, 0, 1), (5, 3, 0, 1), (5, 4, 0, 1), (5, 5, 0, 1);

-- Populating 'dungeon_academica' table
INSERT INTO dungeon_academica (id_dungeon, nome, descricao, id_tema) VALUES
((SELECT id_sala FROM sala_comum WHERE id_setor = 1 AND tem_dungeon = TRUE ORDER BY id_sala ASC LIMIT 1), 'Matemática Quântica                                                   ', 'Uma dungeon onde os números se comportam de maneira imprevisível.                                                                                                                                    ', 1),
((SELECT id_sala FROM sala_comum WHERE id_setor = 2 AND tem_dungeon = TRUE ORDER BY id_sala ASC LIMIT 1), 'Labirinto de Códigos                                                  ', 'Um ambiente complexo cheio de algoritmos e funções enigmáticas.                                                                                                                                      ', 2),
((SELECT id_sala FROM sala_comum WHERE id_setor = 3 AND tem_dungeon = TRUE ORDER BY id_sala ASC LIMIT 1), 'Fundição de Ideias                                                    ', 'Um lugar onde projetos complexos ganham vida e testam os limites da engenharia.                                                                                                                    ', 3),
((SELECT id_sala FROM sala_comum WHERE id_setor = 4 AND tem_dungeon = TRUE ORDER BY id_sala ASC LIMIT 1), 'Debate Filosófico                                                     ', 'Um salão onde as ideias se chocam e a retórica é a principal arma.                                                                                                                                   ', 4),
((SELECT id_sala FROM sala_comum WHERE id_setor = 5 AND tem_dungeon = TRUE ORDER BY id_sala ASC LIMIT 1), 'O Grande Auditório                                                    ', 'Um local de conhecimento vasto e diversificado, onde tudo pode ser aprendido.                                                                                                                       ', 5);

-- Populating 'reliquia' table
INSERT INTO reliquia (nome, descricao, tipo_reliquia, id_tipo_item) VALUES
('Cálculo Infinito                                                      ', 'Uma relíquia que representa o domínio da matemática.                                                                                                                                         ', 'Matemática                                                            ', (SELECT id_item FROM tipo_item WHERE item_tipo = 'Relíquia')),
('Código Fonte Universal                                                ', 'A relíquia que concede o poder de compreender qualquer programa.                                                                                                                             ', 'Programação                                                           ', (SELECT id_item FROM tipo_item WHERE item_tipo = 'Relíquia')),
('Projeto Mestre                                                        ', 'Uma planta que revela os segredos de todas as construções.                                                                                                                                  ', 'Engenharias                                                           ', (SELECT id_item FROM tipo_item WHERE item_tipo = 'Relíquia')),
('Sabedoria Ancestral                                                   ', 'Um tomo com o conhecimento de gerações de pensadores.                                                                                                                                        ', 'Humanidades                                                           ', (SELECT id_item FROM tipo_item WHERE item_tipo = 'Relíquia')),
('Conhecimento Geral Abrangente                                         ', 'A relíquia que unifica todo o saber acadêmico.                                                                                                                                               ', 'Gerais                                                                ', (SELECT id_item FROM tipo_item WHERE item_tipo = 'Relíquia'));

-- Populating 'boss' table
INSERT INTO boss (id_tipo_criatura, id_reliquia, nome, descricao, nivel, vida_max) VALUES
((SELECT id_criatura FROM tipo_criatura WHERE tipo_criatura = 'Boss'), (SELECT id_reliquia FROM reliquia WHERE tipo_reliquia = 'Matemática                                                            '), 'Professor Álgebra                                                     ', 'Um mestre implacável da matemática abstrata.                                                                                                                                          ', 20, 200),
((SELECT id_criatura FROM tipo_criatura WHERE tipo_criatura = 'Boss'), (SELECT id_reliquia FROM reliquia WHERE tipo_reliquia = 'Programação                                                           '), 'O Último Compilador                                                   ', 'O guardião supremo da lógica de programação.                                                                                                                                         ', 20, 220),
((SELECT id_criatura FROM tipo_criatura WHERE tipo_criatura = 'Boss'), (SELECT id_reliquia FROM reliquia WHERE tipo_reliquia = 'Engenharias                                                           '), 'O Gigante de Concreto                                                 ', 'Uma estrutura colossal que testa a engenharia.                                                                                                                                              ', 20, 230),
((SELECT id_criatura FROM tipo_criatura WHERE tipo_criatura = 'Boss'), (SELECT id_reliquia FROM reliquia WHERE tipo_reliquia = 'Humanidades                                                           '), 'A Burocracia Impiedosa                                                ', 'Um sistema complexo que desafia a paciência de todos.                                                                                                                                        ', 20, 210),
((SELECT id_criatura FROM tipo_criatura WHERE tipo_criatura = 'Boss'), (SELECT id_reliquia FROM reliquia WHERE tipo_reliquia = 'Gerais                                                                '), 'A Crise Existencial                                                   ', 'A dúvida que assola todo estudante na reta final.                                                                                                                                            ', 20, 190);

-- Populating 'monstro_simples' table
INSERT INTO monstro_simples (id_tipo_criatura, nome, descricao, nivel, vida_max, xp_tema, qtd_moedas) VALUES
((SELECT id_criatura FROM tipo_criatura WHERE tipo_criatura = 'Monstro'), 'Erro de Sintaxe                                                       ', 'Um pequeno erro que atrapalha o código.                                                                                                                                                      ', 3, 30, 5, 2),
((SELECT id_criatura FROM tipo_criatura WHERE tipo_criatura = 'Monstro'), 'Derivada Confusa                                                      ', 'Uma função matemática que parece não ter fim.                                                                                                                                                ', 5, 45, 7, 3),
((SELECT id_criatura FROM tipo_criatura WHERE tipo_criatura = 'Monstro'), 'Plágio Descarado                                                      ', 'Uma ameaça à originalidade acadêmica.                                                                                                                                                        ', 7, 60, 9, 4),
((SELECT id_criatura FROM tipo_criatura WHERE tipo_criatura = 'Monstro'), 'Fio Solto                                                             ', 'Um defeito simples em uma instalação elétrica.                                                                                                                                               ', 4, 35, 6, 2),
((SELECT id_criatura FROM tipo_criatura WHERE tipo_criatura = 'Monstro'), 'Preguiça Matinal                                                      ', 'A força que impede o estudante de levantar.                                                                                                                                                  ', 6, 50, 8, 3),
((SELECT id_criatura FROM tipo_criatura WHERE tipo_criatura = 'Monstro'), 'Loop Infinito                                                         ', 'Um programa que nunca termina.                                                                                                                                                               ', 9, 70, 12, 5),
((SELECT id_criatura FROM tipo_criatura WHERE tipo_criatura = 'Monstro'), 'Paradoxo Lógico                                                       ', 'Um problema que desafia a razão.                                                                                                                                                             ', 11, 85, 15, 6),
((SELECT id_criatura FROM tipo_criatura WHERE tipo_criatura = 'Monstro'), 'Teoria da Conspiração                                                 ', 'Uma narrativa sem evidências, mas persistente.                                                                                                                                               ', 13, 100, 18, 7),
((SELECT id_criatura FROM tipo_criatura WHERE tipo_criatura = 'Monstro'), 'Solda Fria                                                            ', 'Uma conexão mal feita que causa instabilidade.                                                                                                                                               ', 10, 75, 13, 5),
((SELECT id_criatura FROM tipo_criatura WHERE tipo_criatura = 'Monstro'), 'Distração Coletiva                                                    ', 'O inimigo de toda sessão de estudos.                                                                                                                                                         ', 8, 65, 10, 4);

-- Populating 'Ataque' table
INSERT INTO Ataque (id_tipo_habilidade, id_tema, nome, nivel, coolDown, danoCausado) VALUES
((SELECT id_habilidade FROM tipoHabilidade WHERE tipo_habilidade = 'ataque'), (SELECT id_tema FROM tema WHERE nome = 'Matemática'), 'Equação Quadrática                                                    ', 5, 2, 15),
((SELECT id_habilidade FROM tipoHabilidade WHERE tipo_habilidade = 'ataque'), (SELECT id_tema FROM tema WHERE nome = 'Matemática'), 'Teorema de Pitágoras                                                  ', 8, 3, 20),
((SELECT id_habilidade FROM tipoHabilidade WHERE tipo_habilidade = 'ataque'), (SELECT id_tema FROM tema WHERE nome = 'Programação'), 'Bug Report                                                            ', 6, 2, 16),
((SELECT id_habilidade FROM tipoHabilidade WHERE tipo_habilidade = 'ataque'), (SELECT id_tema FROM tema WHERE nome = 'Programação'), 'Zero Division                                                         ', 18, 6, 35),
((SELECT id_habilidade FROM tipoHabilidade WHERE tipo_habilidade = 'ataque'), (SELECT id_tema FROM tema WHERE nome = 'Engenharias'), 'Desenho Técnico                                                       ', 7, 2, 18),
((SELECT id_habilidade FROM tipoHabilidade WHERE tipo_habilidade = 'ataque'), (SELECT id_tema FROM tema WHERE nome = 'Humanidades'), 'Retórica Persuasiva                                                   ', 5, 2, 14),
((SELECT id_habilidade FROM tipoHabilidade WHERE tipo_habilidade = 'ataque'), (SELECT id_tema FROM tema WHERE nome = 'Gerais'), 'Ataque Básico                                                         ', 1, 1, 8),
((SELECT id_habilidade FROM tipoHabilidade WHERE tipo_habilidade = 'ataque'), (SELECT id_tema FROM tema WHERE nome = 'Matemática'), 'Cálculo Integral                                                      ', 15, 5, 30), 
((SELECT id_habilidade FROM tipoHabilidade WHERE tipo_habilidade = 'ataque'), (SELECT id_tema FROM tema WHERE nome = 'Engenharias'), 'Falha de Projeto                                                      ', 17, 5, 32), 
((SELECT id_habilidade FROM tipoHabilidade WHERE tipo_habilidade = 'ataque'), (SELECT id_tema FROM tema WHERE nome = 'Humanidades'), 'Argumento Irrefutável                                                 ', 16, 5, 28), 
((SELECT id_habilidade FROM tipoHabilidade WHERE tipo_habilidade = 'ataque'), (SELECT id_tema FROM tema WHERE nome = 'Gerais'), 'Estudo Avançado                                                       ', 10, 4, 20);  

-- Populating 'Cura' table
INSERT INTO Cura (id_tipo_habilidade, id_tema, nome, nivel, coolDown, vidaRecuperada) VALUES
((SELECT id_habilidade FROM tipoHabilidade WHERE tipo_habilidade = 'cura'), (SELECT id_tema FROM tema WHERE nome = 'Matemática'), 'Revisão de Conceitos                                                  ', 4, 3, 10),
((SELECT id_habilidade FROM tipoHabilidade WHERE tipo_habilidade = 'cura'), (SELECT id_tema FROM tema WHERE nome = 'Programação'), 'Stack Overflow                                                        ', 5, 3, 12),
((SELECT id_habilidade FROM tipoHabilidade WHERE tipo_habilidade = 'cura'), (SELECT id_tema FROM tema WHERE nome = 'Engenharias'), 'Reparo de Circuito                                                    ', 6, 3, 11),
((SELECT id_habilidade FROM tipoHabilidade WHERE tipo_habilidade = 'cura'), (SELECT id_tema FROM tema WHERE nome = 'Humanidades'), 'Sessão de Terapia                                                     ', 4, 3, 9),
((SELECT id_habilidade FROM tipoHabilidade WHERE tipo_habilidade = 'cura'), (SELECT id_tema FROM tema WHERE nome = 'Gerais'), 'Curativo Simples                                                      ', 1, 1, 5),
((SELECT id_habilidade FROM tipoHabilidade WHERE tipo_habilidade = 'cura'), (SELECT id_tema FROM tema WHERE nome = 'Gerais'), 'Pausa para o Café                                                     ', 7, 2, 15); 

-- Populating 'Defesa' table
INSERT INTO Defesa (id_tipo_habilidade, id_tema, nome, nivel, coolDown, danoMitigado) VALUES
((SELECT id_habilidade FROM tipoHabilidade WHERE tipo_habilidade = 'defesa'), (SELECT id_tema FROM tema WHERE nome = 'Matemática'), 'Defesa Numérica                                                       ', 7, 2, 10),
((SELECT id_habilidade FROM tipoHabilidade WHERE tipo_habilidade = 'defesa'), (SELECT id_tema FROM tema WHERE nome = 'Programação'), 'Firewall Pessoal                                                      ', 9, 2, 13),
((SELECT id_habilidade FROM tipoHabilidade WHERE tipo_habilidade = 'defesa'), (SELECT id_tema FROM tema WHERE nome = 'Engenharias'), 'Material Resistente                                                   ', 8, 2, 11),
((SELECT id_habilidade FROM tipoHabilidade WHERE tipo_habilidade = 'defesa'), (SELECT id_tema FROM tema WHERE nome = 'Humanidades'), 'Escudo Cultural                                                       ', 7, 2, 9),
((SELECT id_habilidade FROM tipoHabilidade WHERE tipo_habilidade = 'defesa'), (SELECT id_tema FROM tema WHERE nome = 'Gerais'), 'Corrida Rápida                                                        ', 2, 1, 7);


-- Populating 'instancia_de_criatura' table
DO $$
DECLARE
    dungeon_rec RECORD;
    monstro_simples_id_val INT;
    boss_id_val INT;
    vida_max_val INT;
    num_instances_simple INT := 9;
BEGIN
    FOR dungeon_rec IN SELECT id_dungeon, id_tema FROM dungeon_academica LOOP
        SELECT b.id_boss, b.vida_max
        INTO boss_id_val, vida_max_val
        FROM boss b
        JOIN reliquia r ON b.id_reliquia = r.id_reliquia
        JOIN tema t ON r.tipo_reliquia = t.nome
        WHERE t.id_tema = dungeon_rec.id_tema
        LIMIT 1;

        IF boss_id_val IS NOT NULL THEN
            INSERT INTO instancia_de_criatura (id_boss, vida_atual, id_dungeon) VALUES
            (boss_id_val, vida_max_val, dungeon_rec.id_dungeon);
        END IF;

        FOR i IN 1..num_instances_simple LOOP
            SELECT ms.id_monstro_simples, ms.vida_max
            INTO monstro_simples_id_val, vida_max_val
            FROM monstro_simples ms
            WHERE ms.nome ILIKE '%' || (CASE dungeon_rec.id_tema
                                        WHEN 1 THEN 'Derivada%'
                                        WHEN 2 THEN 'Erro de Sintaxe%'
                                        WHEN 3 THEN 'Fio Solto%'
                                        WHEN 4 THEN 'Plágio%'
                                        WHEN 5 THEN 'Preguiça%'
                                        END)
            ORDER BY random() LIMIT 1;

            INSERT INTO instancia_de_criatura (id_monstro_simples, vida_atual, id_dungeon) VALUES
            (monstro_simples_id_val, vida_max_val, dungeon_rec.id_dungeon);
        END LOOP;
    END LOOP;
END $$;


-- Populating 'consumivel' table
INSERT INTO consumivel (id_tipo_item, nome, descricao, efeito, preco) VALUES
((SELECT id_item FROM tipo_item WHERE item_tipo = 'Consumível'), 'Café Expresso                                                         ', 'Recupera um pouco de estresse e te dá energia.                                                                                                                                               ', 5.0, 3.0),
((SELECT id_item FROM tipo_item WHERE item_tipo = 'Consumível'), 'Barra de Cereal                                                       ', 'Um lanche rápido para restaurar a vitalidade.                                                                                                                                                ', 10.0, 5.0),
((SELECT id_item FROM tipo_item WHERE item_tipo = 'Consumível'), 'Comprimido Analgésico                                                 ', 'Alivia dores de cabeça e ajuda a focar.                                                                                                                                                      ', 7.0, 4.0),
((SELECT id_item FROM tipo_item WHERE item_tipo = 'Consumível'), 'Guaraná Natural                                                       ', 'Aumenta sua vida por um curto período.                                                                                                                                                       ', 15.0, 8.0),
((SELECT id_item FROM tipo_item WHERE item_tipo = 'Consumível'), 'Chocolate Acadêmico                                                   ', 'Melhora o humor e a concentração.                                                                                                                                                            ', 12.0, 6.0);

-- Populating 'equipavel' table
INSERT INTO equipavel (id_tipo_item, nome, descricao, efeito, preco, equipado) VALUES
((SELECT id_item FROM tipo_item WHERE item_tipo = 'Equipável'), 'Óculos de Leitura Avançada                                            ', 'Aumenta sua vida máxima permanentemente.                                                                                                                                                     ', 10, 50, FALSE),
((SELECT id_item FROM tipo_item WHERE item_tipo = 'Equipável'), 'Mochila de Estudo                                                     ', 'Permite carregar mais itens.                                                                                                                                                                 ', 5, 30, FALSE),
((SELECT id_item FROM tipo_item WHERE item_tipo = 'Equipável'), 'Tênis Confortável                                                     ', 'Aumenta sua capacidade de fuga em combate.                                                                                                                                                   ', 2, 40, FALSE);

-- Populating 'monetario' table
INSERT INTO monetario (id_tipo_item, nome, descricao, valor) VALUES
((SELECT id_item FROM tipo_item WHERE item_tipo = 'Monetário'), 'Moeda Acadêmica                                                       ', 'A moeda corrente do campus.                                                                                                                                                                  ', 1),
((SELECT id_item FROM tipo_item WHERE item_tipo = 'Monetário'), 'Ficha de RU                                                           ', 'Pode ser trocada por refeições.                                                                                                                                                              ', 5);

-- Populating 'loja_item' table (Apenas itens consumíveis nas lojas)
DO $$
DECLARE
    shop_sala_id INT;
    consumivel_id_val INT;
BEGIN
    FOR shop_sala_id IN (SELECT id_sala FROM sala_comum WHERE tem_loja = TRUE) LOOP
        FOR consumivel_id_val IN (SELECT id_consumivel FROM consumivel ORDER BY random() LIMIT 3) LOOP
            INSERT INTO loja_item (id_sala, id_consumivel)
            VALUES (shop_sala_id, consumivel_id_val);
        END LOOP;
    END LOOP;
END $$;

INSERT INTO habilidade_criatura (id_monstro_simples, id_boss, id_habilidade_ataque, id_habilidade_cura, id_habilidade_defesa) VALUES
-- Monstros Simples - Erro de Sintaxe (Programação)
((SELECT id_monstro_simples FROM monstro_simples WHERE TRIM(nome) = TRIM('Erro de Sintaxe') LIMIT 1), NULL, (SELECT id_ataque_habilidade FROM Ataque WHERE TRIM(nome) = TRIM('Bug Report') LIMIT 1), NULL, NULL),
((SELECT id_monstro_simples FROM monstro_simples WHERE TRIM(nome) = TRIM('Erro de Sintaxe') LIMIT 1), NULL, NULL, NULL, (SELECT id_defesa_habilidade FROM Defesa WHERE TRIM(nome) = TRIM('Firewall Pessoal') LIMIT 1)),

-- Monstros Simples - Derivada Confusa (Matemática)
((SELECT id_monstro_simples FROM monstro_simples WHERE TRIM(nome) = TRIM('Derivada Confusa') LIMIT 1), NULL, (SELECT id_ataque_habilidade FROM Ataque WHERE TRIM(nome) = TRIM('Equação Quadrática') LIMIT 1), NULL, NULL),
((SELECT id_monstro_simples FROM monstro_simples WHERE TRIM(nome) = TRIM('Derivada Confusa') LIMIT 1), NULL, NULL, (SELECT id_cura_habilidade FROM Cura WHERE TRIM(nome) = TRIM('Revisão de Conceitos') LIMIT 1), NULL),

-- Monstros Simples - Plágio Descarado (Humanidades)
((SELECT id_monstro_simples FROM monstro_simples WHERE TRIM(nome) = TRIM('Plágio Descarado') LIMIT 1), NULL, (SELECT id_ataque_habilidade FROM Ataque WHERE TRIM(nome) = TRIM('Retórica Persuasiva') LIMIT 1), NULL, NULL),
((SELECT id_monstro_simples FROM monstro_simples WHERE TRIM(nome) = TRIM('Plágio Descarado') LIMIT 1), NULL, NULL, NULL, (SELECT id_defesa_habilidade FROM Defesa WHERE TRIM(nome) = TRIM('Escudo Cultural') LIMIT 1)),

-- Monstros Simples - Fio Solto (Engenharias)
((SELECT id_monstro_simples FROM monstro_simples WHERE TRIM(nome) = TRIM('Fio Solto') LIMIT 1), NULL, (SELECT id_ataque_habilidade FROM Ataque WHERE TRIM(nome) = TRIM('Desenho Técnico') LIMIT 1), NULL, NULL),
((SELECT id_monstro_simples FROM monstro_simples WHERE TRIM(nome) = TRIM('Fio Solto') LIMIT 1), NULL, NULL, (SELECT id_cura_habilidade FROM Cura WHERE TRIM(nome) = TRIM('Reparo de Circuito') LIMIT 1), NULL),

-- Monstros Simples - Preguiça Matinal (Gerais)
((SELECT id_monstro_simples FROM monstro_simples WHERE TRIM(nome) = TRIM('Preguiça Matinal') LIMIT 1), NULL, (SELECT id_ataque_habilidade FROM Ataque WHERE TRIM(nome) = TRIM('Ataque Básico') LIMIT 1), NULL, NULL),
((SELECT id_monstro_simples FROM monstro_simples WHERE TRIM(nome) = TRIM('Preguiça Matinal') LIMIT 1), NULL, NULL, (SELECT id_cura_habilidade FROM Cura WHERE TRIM(nome) = TRIM('Curativo Simples') LIMIT 1), NULL),


-- Bosses - Professor Álgebra (Matemática)
(NULL, (SELECT id_boss FROM boss WHERE TRIM(nome) = TRIM('Professor Álgebra') LIMIT 1), (SELECT id_ataque_habilidade FROM Ataque WHERE TRIM(nome) = TRIM('Cálculo Integral') LIMIT 1), NULL, NULL),
(NULL, (SELECT id_boss FROM boss WHERE TRIM(nome) = TRIM('Professor Álgebra') LIMIT 1), NULL, NULL, (SELECT id_defesa_habilidade FROM Defesa WHERE TRIM(nome) = TRIM('Defesa Numérica') LIMIT 1)),

-- Bosses - O Último Compilador (Programação)
(NULL, (SELECT id_boss FROM boss WHERE TRIM(nome) = TRIM('O Último Compilador') LIMIT 1), (SELECT id_ataque_habilidade FROM Ataque WHERE TRIM(nome) = TRIM('Zero Division') LIMIT 1), NULL, NULL),
(NULL, (SELECT id_boss FROM boss WHERE TRIM(nome) = TRIM('O Último Compilador') LIMIT 1), NULL, NULL, (SELECT id_defesa_habilidade FROM Defesa WHERE TRIM(nome) = TRIM('Firewall Pessoal') LIMIT 1)),

-- Bosses - O Gigante de Concreto (Engenharias)
(NULL, (SELECT id_boss FROM boss WHERE TRIM(nome) = TRIM('O Gigante de Concreto') LIMIT 1), (SELECT id_ataque_habilidade FROM Ataque WHERE TRIM(nome) = TRIM('Falha de Projeto') LIMIT 1), NULL, NULL),
(NULL, (SELECT id_boss FROM boss WHERE TRIM(nome) = TRIM('O Gigante de Concreto') LIMIT 1), NULL, NULL, (SELECT id_defesa_habilidade FROM Defesa WHERE TRIM(nome) = TRIM('Material Resistente') LIMIT 1)),

-- Bosses - A Burocracia Impiedosa (Humanidades)
(NULL, (SELECT id_boss FROM boss WHERE TRIM(nome) = TRIM('A Burocracia Impiedosa') LIMIT 1), (SELECT id_ataque_habilidade FROM Ataque WHERE TRIM(nome) = TRIM('Argumento Irrefutável') LIMIT 1), NULL, NULL),
(NULL, (SELECT id_boss FROM boss WHERE TRIM(nome) = TRIM('A Burocracia Impiedosa') LIMIT 1), NULL, NULL, (SELECT id_defesa_habilidade FROM Defesa WHERE TRIM(nome) = TRIM('Escudo Cultural') LIMIT 1)),

-- Bosses - A Crise Existencial (Gerais)
(NULL, (SELECT id_boss FROM boss WHERE TRIM(nome) = TRIM('A Crise Existencial') LIMIT 1), (SELECT id_ataque_habilidade FROM Ataque WHERE TRIM(nome) = TRIM('Estudo Avançado') LIMIT 1), NULL, NULL),
(NULL, (SELECT id_boss FROM boss WHERE TRIM(nome) = TRIM('A Crise Existencial') LIMIT 1), NULL, (SELECT id_cura_habilidade FROM Cura WHERE TRIM(nome) = TRIM('Pausa para o Café') LIMIT 1), NULL);

-- Populating 'habilidade_estudante' table (AGORA REFERENCIA OS NOVOS IDs GERADOS NAS TABELAS ATAQUE, CURA, DEFESA.)
INSERT INTO habilidade_estudante (id_estudante, id_habilidade_ataque, id_habilidade_cura, id_habilidade_defesa) VALUES
-- Estudante 1
(1, (SELECT id_ataque_habilidade FROM Ataque WHERE nome = 'Ataque Básico                                                         ' LIMIT 1), NULL, NULL),
(1, NULL, NULL, (SELECT id_defesa_habilidade FROM Defesa WHERE nome = 'Corrida Rápida                                                        ' LIMIT 1)),
(1, NULL, (SELECT id_cura_habilidade FROM Cura WHERE nome = 'Curativo Simples                                                      ' LIMIT 1), NULL),
-- Estudante 2
(2, (SELECT id_ataque_habilidade FROM Ataque WHERE nome = 'Ataque Básico                                                         ' LIMIT 1), NULL, NULL),
(2, NULL, NULL, (SELECT id_defesa_habilidade FROM Defesa WHERE nome = 'Corrida Rápida                                                        ' LIMIT 1)),
(2, NULL, (SELECT id_cura_habilidade FROM Cura WHERE nome = 'Curativo Simples                                                      ' LIMIT 1), NULL),
-- Estudante 3
(3, (SELECT id_ataque_habilidade FROM Ataque WHERE nome = 'Ataque Básico                                                         ' LIMIT 1), NULL, NULL),
(3, NULL, NULL, (SELECT id_defesa_habilidade FROM Defesa WHERE nome = 'Corrida Rápida                                                        ' LIMIT 1)),
(3, NULL, (SELECT id_cura_habilidade FROM Cura WHERE nome = 'Curativo Simples                                                      ' LIMIT 1), NULL),
-- Estudante 4
(4, (SELECT id_ataque_habilidade FROM Ataque WHERE nome = 'Ataque Básico                                                         ' LIMIT 1), NULL, NULL),
(4, NULL, NULL, (SELECT id_defesa_habilidade FROM Defesa WHERE nome = 'Corrida Rápida                                                        ' LIMIT 1)),
(4, NULL, (SELECT id_cura_habilidade FROM Cura WHERE nome = 'Curativo Simples                                                      ' LIMIT 1), NULL),
-- Estudante 5
(5, (SELECT id_ataque_habilidade FROM Ataque WHERE nome = 'Ataque Básico                                                         ' LIMIT 1), NULL, NULL),
(5, NULL, NULL, (SELECT id_defesa_habilidade FROM Defesa WHERE nome = 'Corrida Rápida                                                        ' LIMIT 1)),
(5, NULL, (SELECT id_cura_habilidade FROM Cura WHERE nome = 'Curativo Simples                                                      ' LIMIT 1), NULL);


-- Populating 'habilidade_loja' table (AGORA REFERENCIA OS NOVOS IDs GERADOS NAS TABELAS ATAQUE, CURA, DEFESA.)
DO $$
DECLARE
    loja_sala_id INT;
    habilidade_ataque_id INT;
    habilidade_cura_id INT;
    habilidade_defesa_id INT;
BEGIN
    FOR loja_sala_id IN (SELECT id_sala FROM sala_comum WHERE tem_loja = TRUE) LOOP
        -- Tenta adicionar uma habilidade de Ataque aleatória
        SELECT id_ataque_habilidade INTO habilidade_ataque_id FROM Ataque ORDER BY random() LIMIT 1;
        IF habilidade_ataque_id IS NOT NULL THEN
            INSERT INTO habilidade_loja (id_loja, id_habilidade_ataque, id_habilidade_cura, id_habilidade_defesa)
            VALUES (loja_sala_id, habilidade_ataque_id, NULL, NULL);
        END IF;

        -- Tenta adicionar uma habilidade de Cura aleatória
        SELECT id_cura_habilidade INTO habilidade_cura_id FROM Cura ORDER BY random() LIMIT 1;
        IF habilidade_cura_id IS NOT NULL THEN
            INSERT INTO habilidade_loja (id_loja, id_habilidade_ataque, id_habilidade_cura, id_habilidade_defesa)
            VALUES (loja_sala_id, NULL, habilidade_cura_id, NULL);
        END IF;

        -- Tenta adicionar uma habilidade de Defesa aleatória
        SELECT id_defesa_habilidade INTO habilidade_defesa_id FROM Defesa ORDER BY random() LIMIT 1;
        IF habilidade_defesa_id IS NOT NULL THEN
            INSERT INTO habilidade_loja (id_loja, id_habilidade_ataque, id_habilidade_cura, id_habilidade_defesa)
            VALUES (loja_sala_id, NULL, NULL, habilidade_defesa_id);
        END IF;
    END LOOP;
END $$;


-- Populating 'instancia_de_item' table
DO $$
DECLARE
    instance_count INT := 10;
    random_item_id_for_type INT;
    random_sala_id INT;
    random_estudante_id INT;
    random_item_type_name VARCHAR(100);
BEGIN
    FOR i IN 1..instance_count LOOP
        SELECT item_tipo INTO random_item_type_name FROM tipo_item ORDER BY random() LIMIT 1;

        CASE random_item_type_name
            WHEN 'Consumível' THEN SELECT id_consumivel INTO random_item_id_for_type FROM consumivel ORDER BY random() LIMIT 1;
            WHEN 'Equipável' THEN SELECT id_equipavel INTO random_item_id_for_type FROM equipavel ORDER BY random() LIMIT 1;
            WHEN 'Monetário' THEN SELECT id_monetario INTO random_item_id_for_type FROM monetario ORDER BY random() LIMIT 1;
            WHEN 'Relíquia' THEN SELECT id_reliquia INTO random_item_id_for_type FROM reliquia ORDER BY random() LIMIT 1;
            ELSE random_item_id_for_type := NULL;
        END CASE;

        SELECT id_sala INTO random_sala_id FROM sala_comum ORDER BY random() LIMIT 1;
        SELECT id_estudante INTO random_estudante_id FROM estudante ORDER BY random() LIMIT 1;

        IF random_item_type_name = 'Consumível' THEN
            INSERT INTO instancia_de_item (id_consumivel, id_sala, id_estudante) VALUES (random_item_id_for_type, random_sala_id, random_estudante_id);
        ELSIF random_item_type_name = 'Equipável' THEN
            INSERT INTO instancia_de_item (id_equipavel, id_sala, id_estudante) VALUES (random_item_id_for_type, random_sala_id, random_estudante_id);
        ELSIF random_item_type_name = 'Monetário' THEN
            INSERT INTO instancia_de_item (id_monetario, id_sala, id_estudante) VALUES (random_item_id_for_type, random_sala_id, random_estudante_id);
        ELSIF random_item_type_name = 'Relíquia' THEN
            INSERT INTO instancia_de_item (id_reliquia, id_sala, id_estudante) VALUES (random_item_id_for_type, random_sala_id, random_estudante_id);
        END IF;

    END LOOP;
END $$;