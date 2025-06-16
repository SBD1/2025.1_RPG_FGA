# DML

DML (Data Manipulation Language) é a parte da linguagem SQL usada para inserir, atualizar, deletar e manipular dados dentro das tabelas de um banco de dados.

Neste contexto, o script `DML.sql` foi utilizado para popular o banco de dados com dados iniciais, simulando um ambiente completo de um RPG acadêmico baseado em temas universitários da Universidade de Brasília (UnB);

## Operações realizadas

### Inserção de temas

```sql
INSERT INTO tema (nome) VALUES
('Matemática'), ('Programação'), ('Engenharias'), ('Humanidades'), ('Gerais');
```
Cada tema representa uma área do conhecimento presente no RPG.

---

### Inserção de habilidades

```sql
INSERT INTO habilidades (nome, tipo_habilidade, nivel, coolDown, id_tema) VALUES
('Equação Quadrática', 'A', 5, 2, 1), ...
```
As habilidades são divididas por tipo:
- `A` = Ataque
- `D` = Defesa
- `C` = Cura

---

### Inserção de criaturas

```sql
INSERT INTO criatura (nivel, vida_max, tipo_criatura, nome, descricao) VALUES
(3, 30, 'Monstro Simples', 'Erro de Sintaxe', '...'), ...
```
Inclui monstros simples (nível ≤ 15) e bosses (nível = 20).

---

### Inserção de campus e setores

```sql
INSERT INTO campus (nome, descricao) VALUES
('UnB Campus Gama', '...');
```
Os setores são interligados de forma circular com `id_proxSetor` e `id_prevSetor`.

---

### Geração de salas comuns com lojas e dungeons

```sql
DO $$
DECLARE ...
BEGIN
    -- gera 10 salas por setor
END $$;
```
Cada setor possui 10 salas, com pelo menos uma loja e uma dungeon.

---

### Inserção de estudantes e suas afinidades

```sql
INSERT INTO estudante (...) VALUES
(1, 'Alice Dev', 20, 20, 10), ...
```
Cada estudante começa com afinidade nível 1 e 0 XP para cada tema.

---

### Inserção de itens
```sql
INSERT INTO item (nome, descricao, item_tipo) VALUES
-- Consumíveis 
...
-- Equipáveis (Não Consumíveis) 
...
-- Monetário 
...
```
---

### Inserção de lojas

```sql
INSERT INTO loja (nome) VALUES
('Loja UED Materiais'), ...
```
Cada loja recebe itens consumíveis aleatórios.

---

### Inserção de habilidades de criaturas e de estudantes

```sql
NSERT INTO habilidade_criatura (id_criatura, id_habilidade) VALUES
...

INSERT INTO habilidade_estudante (id_estudante, id_habilidade) VALUES
...
```
Cada criatura recebe habilidades compatíveis com seu tema. 
Estudantes começam com habilidades básicas como "Ataque Básico", "Curativo Simples" e "Corrida Rápida".

---

### Inserção de dungeons e seus bosses

```sql
INSERT INTO dungeon_academica (...) VALUES
...

INSERT INTO boss (id_boss, id_reliquia) VALUES
...
```
Cada dungeon é vinculada a um tema e tem um boss, que por sua vez carrega uma relíquia.

---

### Inserção de habilidades ofensivas, defensivas e de cura

```sql
INSERT INTO Ataque (...), INSERT INTO Defesa (...), INSERT INTO Cura (...)
```
Define as propriedades específicas das habilidades por tipo (ex: dano causado, mitigado ou vida recuperada).

---

### Histórico de Versões

| Versão | Data       | Descrição                           | Autor              |
|--------|------------|-------------------------------------|--------------------|
| 1.0    | 12/06/2025 | Carga inicial de dados no sistema   | Rodrigo Amaral     |