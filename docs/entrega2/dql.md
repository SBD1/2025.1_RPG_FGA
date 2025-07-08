
# DQL 

DQL (Data Query Language) é uma parte da linguagem SQL (Structured Query Language) usada para consultar dados de um banco de dados. O objetivo principal do DQL é recuperar ou consultar informações armazenadas nas tabelas do banco de dados.

## Consultas que serão utilizadas

### **scripts/jogo/combate**

#### **main.py**

##### Habilidades do estudante  
```sql
SELECT he.id_habilidade,
       th.tipo_habilidade,
       COALESCE(a.nome, c.nome, d.nome) AS nome,
       COALESCE(a.nivel, c.nivel, d.nivel) AS nivel,
       COALESCE(a.coolDown, c.coolDown, d.coolDown) AS cooldown,
       a.danoCausado,
       c.vidaRecuperada,
       d.danoMitigado,
       t.nome AS tema
FROM habilidade_estudante he
JOIN tipoHabilidade th ON he.id_habilidade = th.id_habilidade
LEFT JOIN Ataque a ON he.id_habilidade = a.id_habilidade
LEFT JOIN Cura c ON he.id_habilidade = c.id_habilidade
LEFT JOIN Defesa d ON he.id_habilidade = d.id_habilidade
JOIN tema t ON COALESCE(a.id_tema, c.id_tema, d.id_tema) = t.id_tema
WHERE he.id_estudante = %s
```

##### Habilidades da criatura  
```sql
SELECT hc.id_habilidade,
       th.tipo_habilidade,
       COALESCE(a.nome, c.nome, d.nome) AS nome,
       COALESCE(a.nivel, c.nivel, d.nivel) AS nivel,
       COALESCE(a.coolDown, c.coolDown, d.coolDown) AS cooldown,
       a.danoCausado,
       c.vidaRecuperada,
       d.danoMitigado,
       t.nome AS tema
FROM habilidade_criatura hc
JOIN tipoHabilidade th ON hc.id_habilidade = th.id_habilidade
LEFT JOIN Ataque a ON hc.id_habilidade = a.id_habilidade
LEFT JOIN Cura c ON hc.id_habilidade = c.id_habilidade
LEFT JOIN Defesa d ON hc.id_habilidade = d.id_habilidade
JOIN tema t ON COALESCE(a.id_tema, c.id_tema, d.id_tema) = t.id_tema
WHERE hc.id_criatura = %s
```

##### Vida atual do estudante  
```sql
SELECT vida FROM estudante WHERE id_estudante = %s
```

##### Vida máxima da criatura (Monstro ou Boss)  
```sql
SELECT vida_max FROM monstro_simples WHERE id_criatura = %s
UNION
SELECT vida_max FROM boss WHERE id_criatura = %s
```

---

### **scripts/jogo/map**

#### **dungeon.py**

##### Detalhes da dungeon na sala  
```sql
SELECT s.tem_dungeon, d.id_dungeon, d.nome, d.descricao, d.id_tema, t.nome
FROM sala_comum s
JOIN dungeon_academica d ON d.id_dungeon = s.id_sala
JOIN tema t ON d.id_tema = t.id_tema
WHERE s.id_sala = %s
```

##### Detalhes do boss e sua relíquia  
```sql
SELECT b.id_criatura, b.nome, b.descricao, b.nivel, b.vida_max, b.id_reliquia, r.nome
FROM boss b
JOIN reliquia r ON b.id_reliquia = r.id_reliquia
WHERE b.id_criatura = %s
```

##### Verificar posse de relíquia pelo estudante  
```sql
SELECT 1
FROM instancia_de_item ii
JOIN reliquia r ON ii.id_item = r.id_reliquia
WHERE ii.id_estudante = %s AND r.id_reliquia = %s
LIMIT 1
```

##### Listar monstros instanciados na dungeon  
```sql
SELECT m.id_criatura, m.nome, m.descricao, m.nivel, m.vida_max,
       ic.vida_atual, m.qtd_moedas, m.xp_tema
FROM instancia_de_criatura ic
JOIN monstro_simples m ON ic.id_criatura = m.id_criatura
WHERE ic.id_dungeon = %s
```

---

#### **loja.py**

##### Consumíveis disponíveis na loja  
```sql
SELECT i.id_item, c.nome, c.descricao, c.preco
FROM loja_item li
JOIN tipo_item i ON li.id_item = i.id_item
JOIN consumivel c ON i.id_item = c.id_item
WHERE li.id_sala = %s
```

##### Habilidades disponíveis na loja  
```sql
SELECT 
    th.id_habilidade, 
    COALESCE(a.nome, c.nome, d.nome) AS nome,
    th.tipo_habilidade,
    COALESCE(a.preco, c.preco, d.preco) AS preco,
    t.nome AS nome_tema,
    COALESCE(a.nivel, c.nivel, d.nivel) AS nivel_req,
    t.id_tema
FROM habilidade_loja hl
JOIN tipoHabilidade th ON hl.id_habilidade = th.id_habilidade
LEFT JOIN Ataque a ON hl.id_habilidade = a.id_habilidade
LEFT JOIN Cura c ON hl.id_habilidade = c.id_habilidade
LEFT JOIN Defesa d ON hl.id_habilidade = d.id_habilidade
LEFT JOIN tema t ON COALESCE(a.id_tema, c.id_tema, d.id_tema) = t.id_tema
WHERE hl.id_loja = %s
```

##### Nível de afinidade do estudante  
```sql
SELECT nivel_atual FROM afinidade WHERE id_estudante = %s AND id_tema = %s
```

##### Verificar se estudante já possui a habilidade  
```sql
SELECT 1 FROM habilidade_estudante WHERE id_estudante = %s AND id_habilidade = %s
```

##### Verificar se a sala possui loja  
```sql
SELECT tem_loja FROM sala_comum WHERE id_sala = %s
```

---

#### **sala.py**

##### Sala atual do estudante  
```sql
SELECT id_sala FROM estudante WHERE id_estudante = %s
```

##### Salas adjacentes (anterior / próxima)  
```sql
SELECT s.id_sala, s.nome, s.descricao, c.nome as campus
FROM sala_comum s
JOIN setor st ON s.id_setor = st.id_setor
JOIN campus c ON st.id_campus = c.id_campus
WHERE s.id_sala IN (
    SELECT id_prevSala FROM sala_comum WHERE id_sala = %s
    UNION
    SELECT id_proxSala FROM sala_comum WHERE id_sala = %s
)
ORDER BY s.id_sala
```

##### Nome do estudante e da sala  
```sql
SELECT e.nome, s.nome
FROM Estudante e
JOIN Sala_Comum s ON e.id_sala = s.id_sala
WHERE e.id_estudante = %s
```

##### Nome da sala  
```sql
SELECT nome FROM Sala_Comum WHERE id_sala = %s
```

##### Verificar presença de dungeon ou loja na sala  
```sql
SELECT tem_dungeon, tem_loja FROM sala_comum WHERE id_sala = %s
```

##### Itens disponíveis na sala (não coletados)  
```sql
SELECT
    ii.id_instanciaItem,
    COALESCE(c.nome, e.nome, m.nome) AS nome_item
FROM instancia_de_item ii
JOIN tipo_item ti ON ii.id_item = ti.id_item
LEFT JOIN consumivel c ON ti.id_item = c.id_item
LEFT JOIN equipavel e ON ti.id_item = e.id_item
LEFT JOIN monetario m ON ti.id_item = m.id_item
WHERE ii.id_sala = %s AND ii.id_estudante IS NULL
```

---

#### **setor.py**

##### Sala atual do estudante  
```sql
SELECT id_sala FROM estudante WHERE id_estudante = %s
```

##### Setor da sala  
```sql
SELECT id_setor FROM sala_comum WHERE id_sala = %s
```

##### Setores adjacentes do setor atual  
```sql
SELECT id_prevsetor, id_proxsetor FROM setor WHERE id_setor = %s
```

##### Informações de múltiplos setores  
```sql
SELECT id_setor, nome, descricao FROM setor WHERE id_setor = ANY(%s)
```

##### Primeira sala do setor  
```sql
SELECT id_sala, nome FROM sala_comum WHERE id_setor = %s ORDER BY id_sala LIMIT 1
```

---

### **scripts/jogo/monster**

#### **boss.py**

##### Boss instanciado na dungeon (detalhes completos)  
```sql
SELECT
    b.id_criatura,
    b.nome,
    b.descricao,
    b.nivel,
    b.vida_max,
    r.id_reliquia,
    r.nome AS nome_reliquia,
    r.descricao AS desc_reliquia,
    r.tipo_reliquia,
    ic.id_instanciaCriatura,
    ic.vida_atual
FROM instancia_de_criatura ic
JOIN boss b ON b.id_criatura = ic.id_criatura
JOIN reliquia r ON r.id_reliquia = b.id_reliquia
WHERE ic.id_dungeon = %s
LIMIT 1
```

#### **monster.py**

##### Habilidades da criatura (genéricas)  
```sql
SELECT
    hc.id_habilidade,
    th.tipo_habilidade,
    COALESCE(a.nome, c.nome, d.nome) AS nome,
    COALESCE(a.nivel, c.nivel, d.nivel) AS nivel,
    COALESCE(a.coolDown, c.coolDown, d.coolDown) AS cooldown,
    a.danoCausado,
    c.vidaRecuperada,
    d.danoMitigado,
    COALESCE(a.id_tema, c.id_tema, d.id_tema) AS id_tema
FROM habilidade_criatura hc
JOIN tipoHabilidade th ON hc.id_habilidade = th.id_habilidade
LEFT JOIN Ataque a ON hc.id_habilidade = a.id_habilidade
LEFT JOIN Cura c ON hc.id_habilidade = c.id_habilidade
LEFT JOIN Defesa d ON hc.id_habilidade = d.id_habilidade
WHERE hc.id_criatura = %s
```

---

### **scripts/jogo/player**

#### **afinidade.py**

##### Afinidades do estudante  
```sql
SELECT a.id_tema, t.nome AS nome_tema, a.nivel_atual, a.xp_atual
FROM afinidade a
JOIN tema t ON a.id_tema = t.id_tema
WHERE a.id_estudante = %s
ORDER BY a.id_tema
```

#### **consumir.py**

##### Efeito do consumível instanciado  
```sql
SELECT c.efeito
FROM instancia_de_item ci
JOIN consumivel c ON ci.id_item = c.id_item
WHERE ci.id_instanciaItem = %s
  AND ci.id_estudante = %s
```

#### **habilidades.py**

##### Habilidades do estudante  
```sql
SELECT
    he.id_habilidade,
    th.tipo_habilidade,
    COALESCE(a.nome, c.nome, d.nome) AS nome,
    COALESCE(a.nivel, c.nivel, d.nivel) AS nivel,
    COALESCE(a.coolDown, c.coolDown, d.coolDown) AS cooldown,
    a.danoCausado,
    c.vidaRecuperada,
    d.danoMitigado,
    tm.nome AS nome_tema
FROM habilidade_estudante he
JOIN tipoHabilidade th ON he.id_habilidade = th.id_habilidade
LEFT JOIN Ataque a ON he.id_habilidade = a.id_habilidade
LEFT JOIN Cura c ON he.id_habilidade = c.id_habilidade
LEFT JOIN Defesa d ON he.id_habilidade = d.id_habilidade
LEFT JOIN tema tm ON COALESCE(a.id_tema, c.id_tema, d.id_tema) = tm.id_tema
WHERE he.id_estudante = %s
```

#### **inventario.py**

##### Consumíveis do estudante  
```sql
SELECT ci.id_instanciaItem,
       c.nome AS nome_item,
       c.descricao,
       c.efeito,
       c.preco
FROM instancia_de_item ci
JOIN consumivel c ON ci.id_item = c.id_item
WHERE ci.id_estudante = %s
```

##### Equipáveis do estudante  
```sql
SELECT ei.id_instanciaItem,
       e.nome AS nome_item,
       e.descricao,
       e.efeito,
       e.preco,
       ei.equipado
FROM instancia_de_item ei
JOIN equipavel e ON ei.id_item = e.id_item
WHERE ei.id_estudante = %s
```

##### Relíquias do estudante  
```sql
SELECT ri.id_instanciaItem,
       r.nome AS nome_reliquia,
       r.descricao,
       r.tipo_reliquia
FROM instancia_de_item ri
JOIN reliquia r ON ri.id_item = r.id_reliquia
WHERE ri.id_estudante = %s
```

##### Itens monetários do estudante  
```sql
SELECT mi.id_instanciaItem,
       m.nome AS nome_item,
       m.descricao,
       m.valor
FROM instancia_de_item mi
JOIN monetario m ON mi.id_item = m.id_item
WHERE mi.id_estudante = %s
```

#### **menu.py**

##### Status do estudante e sua sala  
```sql
SELECT e.nome, e.vida, e.estresse, e.total_dinheiro, s.nome AS nome_sala, e.id_sala
FROM estudante e
JOIN sala_comum s ON e.id_sala = s.id_sala
WHERE e.id_estudante = %s
```

---

### **scripts/jogo**

#### **debug_menu.py**

##### Salas com dungeon  
```sql
SELECT s.id_sala, s.nome, st.nome AS nome_setor
FROM sala_comum s
JOIN setor st ON s.id_setor = st.id_setor
WHERE s.tem_dungeon = TRUE
ORDER BY s.id_sala
```

##### Salas com loja  
```sql
SELECT s.id_sala, s.nome, st.nome AS nome_setor
FROM sala_comum s
JOIN setor st ON s.id_setor = st.id_setor
WHERE s.tem_loja = TRUE
ORDER BY s.id_sala
```

##### Salas com itens disponíveis (quantidade)  
```sql
SELECT s.id_sala, s.nome, COUNT(ii.id_instanciaItem) AS quantidade_itens
FROM sala_comum s
JOIN instancia_de_item ii ON s.id_sala = ii.id_sala
WHERE ii.id_estudante IS NULL
GROUP BY s.id_sala, s.nome
ORDER BY s.id_sala
```

##### Estudantes e suas localizações  
```sql
SELECT
    e.nome AS nome_jogador,
    s.nome AS nome_sala,
    st.nome AS nome_setor
FROM estudante e
JOIN sala_comum s ON e.id_sala = s.id_sala
JOIN setor st ON s.id_setor = st.id_setor
ORDER BY e.id_estudante
```

##### Relacionar salas que possuem dungeon  
```sql
SELECT
    s.id_sala,
    s.nome AS nome_sala,
    d.nome AS nome_dungeon,
    t.nome AS nome_tema
FROM
    sala_comum s
JOIN
    dungeon_academica d ON d.id_dungeon = s.id_sala
JOIN
    tema t ON d.id_tema = t.id_tema
ORDER BY
    s.id_sala
```

---

### **scripts**

#### **app.py**

##### Listar todos os estudantes  
```sql
SELECT id_estudante, nome FROM estudante ORDER BY id_estudante
```

##### Status do estudante e sua sala  
```sql
SELECT e.nome, e.vida, e.estresse, e.total_dinheiro, s.nome AS nome_sala, e.id_sala
FROM estudante e
JOIN sala_comum s ON e.id_sala = s.id_sala
WHERE e.id_estudante = %s
```

#### **temp.py**

### Todas as dungeons e suas salas  
```sql
SELECT s.id_sala, s.nome AS nome_sala, d.nome AS nome_dungeon, d.descricao
FROM sala_comum s
JOIN dungeon_academica d ON s.id_sala = d.id_dungeon
ORDER BY s.id_sala
```

## Histórico de Versões
| Versão |  Data  | Descrição| Autor                 |
| :----: | :--------: | ---------------------------------- | -------------------------------------------------------------------------------- |
| `1.0` | 12/06/2025 | Criação das consultas     | [Ludmila Nunes](https://github.com/ludmilaaysha) & [Isaque Camargos](https://github.com/isaqzin)|
| `2.0` | 07/07/2025 | Consultas finais     | [Ludmila Nunes](https://github.com/ludmilaaysha) & [Isaque Camargos](https://github.com/isaqzin)|