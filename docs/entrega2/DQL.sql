-- --------------------------------------------------------------------------------------
-- Data Criacao ...........: 12/06/2025                                                --
-- Autor(es) ..............: Isaque Camargos Nascimento e Ludmila Aysha Oliveira Nunes                                                                                  --
-- Versao ..............: 1.0                                                          --
-- Banco de Dados .........: PostgreSQL                                                --
-- Descricao .........: Consulta das tabelas do banco de dados.                        --
-- --------------------------------------------------------------------------------------
-- | Atualizacao : xx/xx/xxxx | Autor(es):         |  --
--                            | Descricao: Inclusão das consultas do banco de dados |  --
-- --------------------------------------------------------------------------------------


-- Consulta para obter os dados de um estudante em específico
SELECT e.*, t.nome AS nome_tema, a.nivel_atual, a.xp_atual
FROM estudante e join afinidade a ON e.id_estudante = a.id_estudante
JOIN tema t ON a.id_tema = t.id_tema
WHERE e.id_estudante = %s;


-- Consulta para obter os dados das habilidades de ataque de um estudante em especifico 
SELECT h.id_habilidade, h.nome, h.nivel, h.coolDown, t.nome AS nome_tema, a.danoCausado, a.porcentagemAcerto
FROM habilidade_estudante he
JOIN habilidades h ON he.id_habilidade = h.id_habilidade
JOIN ataque a ON h.id_habilidade = a.id_habilidade
JOIN tema t ON h.id_tema = t.id_tema
WHERE he.id_estudante = %s;


-- Consulta para obter os dados das habilidades de cura de um estudante em especifico
SELECT h.id_habilidade, h.nome, h.nivel, h.coolDown, t.nome AS nome_tema, c.vidaRecuperada
FROM habilidade_estudante he
JOIN habilidades h ON he.id_habilidade = h.id_habilidade
JOIN cura c ON h.id_habilidade = c.id_habilidade
JOIN tema t ON h.id_tema = t.id_tema
WHERE he.id_estudante = %s;

-- Consulta para obter os dados das habilidades de defesa de um estudante em especifico
SELECT h.id_habilidade, h.nome, h.nivel, h.coolDown, t.nome AS nome_tema, d.danoMitigado
FROM habilidade_estudante he
JOIN habilidades h ON he.id_habilidade = h.id_habilidade
JOIN defesa d ON h.id_habilidade = d.id_habilidade
JOIN tema t ON h.id_tema = t.id_tema
WHERE he.id_estudante = %s;


-- Consulta para obter os dados dos itens consumiveis de um estudante em especifico
SELECT i.id_item, i.nome, i.descricao, i.item_tipo, c.efeito, c.preco
FROM instancia_de_item ii
JOIN item i ON ii.id_item = i.id_item
JOIN consumivel c ON i.id_item = c.id_item
WHERE ii.id_estudante = %s;

-- Consulta para obter os dados dos itens equipaveis de um estudante em especifico
SELECT i.id_item, i.nome, i.descricao, i.item_tipo, e.efeito, e.preco, e.equipado
FROM instancia_de_item ii
JOIN item i ON ii.id_item = i.id_item
JOIN equipavel e ON i.id_item = e.id_item
WHERE ii.id_estudante = %s;

-- Consulta para obter os dados das reliquias de um estudante em especifico
SELECT i.id_item, i.nome, i.descricao, i.item_tipo, r.id_item, r.tipo
FROM instancia_de_item ii
JOIN item i ON ii.id_item = i.id_item
JOIN reliquia r ON i.id_item = r.id_item
WHERE ii.id_estudante = %s;


-- Consulta para obter os dados dos campus e os setores dentro de um campus especifico
SELECT c.*, s.id_setor, s.nome, s.descricao 
FROM campus c
JOIN setor s ON c.id_campus = s.id_campus
WHERE c.id_campus = %s;

-- Consulta para obter os dados de um setor especifico
SELECT *
FROM setor
WHERE id_setor = %s;

-- Consulta para obter os dados de todas as salas de um setor especifico
SELECT *
FROM sala_comum
WHERE id_setor = %s;

-- Consulta para obter os dados de todos os itens equipaveis de uma sala especifica
SELECT i.id_item, i.nome, i.descricao, i.item_tipo, c.efeito, c.preco
FROM instancia_de_item ii
JOIN item i ON ii.id_item = i.id_item
JOIN consumivel c ON i.id_item = c.id_item
WHERE ii.id_sala = %s;


-- Consulta para obter os dados de todos os itens consumiveis de uma sala especifica
SELECT i.id_item, i.nome, i.descricao, i.item_tipo, e.efeito, e.preco, e.equipado
FROM instancia_de_item ii
JOIN item i ON ii.id_item = i.id_item
JOIN equipavel e ON i.id_item = e.id_item
WHERE ii.id_sala = %s;

-- Consulta para obter as habilidades de Ataque disponíveis em uma loja específica
SELECT h.id_habilidade, h.nome, h.nivel, h.coolDown, a.danoCausado, a.porcentagemAcerto
FROM habilidade_loja hl
JOIN habilidades h ON hl.id_habilidade = h.id_habilidade
JOIN Ataque a ON h.id_habilidade = a.id_habilidade
WHERE hl.id_loja = %s;

-- Consulta para obter as habilidades de Cura disponíveis em uma loja específica
SELECT h.id_habilidade, h.nome, h.nivel, h.coolDown, c.vidaRecuperada
FROM habilidade_loja hl
JOIN habilidades h ON hl.id_habilidade = h.id_habilidade
JOIN Cura c ON h.id_habilidade = c.id_habilidade
WHERE hl.id_loja = %s;

-- Consulta para obter as habilidades de Defesa disponíveis em uma loja específica
SELECT h.id_habilidade, h.nome, h.nivel, h.coolDown, d.danoMitigado
FROM habilidade_loja hl
JOIN habilidades h ON hl.id_habilidade = h.id_habilidade
JOIN Defesa d ON h.id_habilidade = d.id_habilidade
WHERE hl.id_loja = %s;


-- Consulta para obter os itens consumiveis disponíveis em uma loja específica
SELECT i.id_item, i.nome, i.descricao, i.item_tipo, c.efeito, c.preco
FROM loja_item li
JOIN item i ON li.id_item = i.id_item
JOIN consumivel c ON i.id_item = c.id_item
WHERE li.id_sala = %s;

-- Consulta para obter os itens equipaveis disponíveis em uma loja específica
SELECT i.id_item, i.nome, i.descricao, i.item_tipo, e.efeito, e.preco, e.equipado
FROM loja_item li
JOIN item i ON li.id_item = i.id_item
JOIN equipavel e ON i.id_item = e.id_item
WHERE li.id_sala = %s;

-- Consulta para obter os dados de uma dungeon especifica
SELECT d.id_dungeon, d.nome, d.descricao, t.nome AS nome_tema
FROM dungeon_academica d
JOIN tema t ON d.id_tema = t.id_tema
WHERE d.id_dungeon = %s;

-- Consulta para obter os dados de todos os monstros simples de uma dungeon em especifico
SELECT ic.vida_atual, c.id_criatura, c.nivel, c.vida_max, c.tipo_criatura, c.nome, c.descricao, ms.xp_tema, ms.qtd_moedas
FROM instancia_de_criatura ic JOIN criatura c ON ic.id_criatura = c.id_criatura
JOIN monstro_simples ms ON c.id_criatura = ms.id_criatura
WHERE ic.id_dungeon = %s;

-- Consulta para obter os dados do boss de uma dungeon em especifico
SELECT ic.vida_atual, c.id_criatura, c.nivel, c.vida_max, c.tipo_criatura, c.nome, c.descricao
FROM instancia_de_criatura ic JOIN criatura c ON ic.id_criatura = c.id_criatura
JOIN boss b ON c.id_criatura = b.id_boss
WHERE ic.id_dungeon = %s;

-- Consulta para obter os dados de todas as habilidades de ataque de uma criatura em especifico
SELECT h.id_habilidade, h.nome, h.nivel, h.coolDown, t.nome AS nome_tema, a.danoCausado, a.porcentagemAcerto
FROM habilidade_criatura hc
JOIN habilidades h ON hc.id_habilidade = h.id_habilidade
JOIN ataque a ON h.id_habilidade = a.id_habilidade
JOIN tema t ON h.id_tema = t.id_tema
WHERE hc.id_criatura = %s;


-- Consulta para obter os dados de todas as habilidades de cura de uma criatura em especifico
SELECT h.id_habilidade, h.nome, h.nivel, h.coolDown, t.nome AS nome_tema, c.vidaRecuperada
FROM habilidade_criatura hc
JOIN habilidades h ON hc.id_habilidade = h.id_habilidade
JOIN cura c ON h.id_habilidade = c.id_habilidade
JOIN tema t ON h.id_tema = t.id_tema
WHERE hc.id_criatura = %s;


-- Consulta para obter os dados de todas as habilidades de defesa de uma criatura em especifico
SELECT h.id_habilidade, h.nome, h.nivel, h.coolDown, t.nome AS nome_tema, d.danoMitigado
FROM habilidade_criatura hc
JOIN habilidades h ON hc.id_habilidade = h.id_habilidade
JOIN defesa d ON h.id_habilidade = d.id_habilidade
JOIN tema t ON h.id_tema = t.id_tema
WHERE hc.id_criatura = %s;

