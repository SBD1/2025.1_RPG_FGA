-- Inserindo temas
INSERT INTO tema (nome) VALUES
('Magia Elemental'),
('Tecnologia Antiga'),
('Biologia Mística');

-- Inserindo habilidades
INSERT INTO habilidades (nome, tipo_habilidade, nivel, coolDown, id_tema) VALUES
('Bola de Fogo', 'Ataque', 1, 2, 1),
('Campo de Força', 'Defesa', 2, 3, 2),
('Regeneração', 'Cura', 1, 4, 3);

-- Inserindo criaturas
INSERT INTO criatura (nivel, vida_max, tipo_criatura, nome, descricao) VALUES
(1, 100, 'Fogo', 'Salamandra Flamejante', 'Criatura feita de fogo'),
(2, 150, 'Tecnológica', 'Autômato Antigo', 'Máquina esquecida dos tempos antigos');

-- Inserindo campus
INSERT INTO campus (nome, descricao) VALUES
('Campus Central', 'O principal centro acadêmico'),
('Campus Norte', 'Especializado em estudos mágicos');

-- Inserindo setores
INSERT INTO setor (id_campus, nome, descricao) VALUES
(1, 'Setor A', 'Setor de entrada do campus'),
(1, 'Setor B', 'Área de estudos intermediários');

-- Inserindo sala_comum
INSERT INTO sala_comum (id_setor, descricao, nome, tem_loja, tem_dungeon) VALUES
(1, 'Sala de descanso com loja', 'Sala Relax', TRUE, FALSE),
(2, 'Sala perigosa com acesso à dungeon', 'Sala Desafio', FALSE, TRUE);

-- Inserindo estudantes
INSERT INTO estudante (id_sala, nome, vida, estresse, total_dinheiro) VALUES
(1, 'Ana Clara', 80, 10, 150),
(2, 'João Pedro', 60, 20, 80);

-- Inserindo afinidades
INSERT INTO afinidade (id_estudante, id_tema, xp_atual, nivel_atual) VALUES
(1, 1, 120, 2),
(2, 3, 90, 1);

-- Inserindo dungeon
INSERT INTO dungeon_academica (nome, descricao, id_tema) VALUES
('Masmorra da Chama', 'Desafios baseados em fogo', 1);

-- Inserindo relíquias
INSERT INTO reliquia (tipo) VALUES
('Amuleto Antigo'),
('Grimório Arcano');

-- Inserindo boss
INSERT INTO boss (id_reliquia) VALUES
(1), (2);

-- Inserindo item
INSERT INTO item (nome, descricao, item_tipo) VALUES
('Poção de Cura', 'Recupera pontos de vida', 'Consumível'),
('Espada de Treinamento', 'Equipamento básico de ataque', 'Equipável');

-- Inserindo consumível e equipável
INSERT INTO consumivel (id_item, efeito, preco) VALUES
(1, 30.5, 50.0);

INSERT INTO equipavel (id_item, efeito, preco, equipado) VALUES
(2, 10, 75, FALSE);

-- Inserindo loja
INSERT INTO loja (nome) VALUES
('Loja Mística');

-- Inserindo habilidade_loja
INSERT INTO habilidade_loja (id_loja, id_habilidade) VALUES
(1, 1),
(1, 3);

-- Inserindo ataques, curas e defesas
INSERT INTO Ataque (id_habilidade, danoCausado, porcentagemAcerto) VALUES
(1, 25, 0.85);

INSERT INTO Cura (id_habilidade, vidaRecuperada) VALUES
(3, 20);

INSERT INTO Defesa (id_habilidade, danoMitigado) VALUES
(2, 15);
