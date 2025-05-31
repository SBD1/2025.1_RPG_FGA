
-- --------------------------------------------------------------------------------------
-- Data Criacao ...........: xx/xx/xxxx                                                --
-- Autor(es) ..............:                                                           --
-- Versao ..............: 1.0                                                          --
-- Banco de Dados .........: PostgreSQL                                                --
-- Descricao .........: Inclusão de CREATE TABLE de todas as tabelas do banco de dados.--
-- --------------------------------------------------------------------------------------
-- | Atualizacao : xx/xx/xxxx | Autor(es):                                      |      --
--                            | Descricao: Inclusão das linhas de CREATE TABLE  |      --
-- | Atualizacao : xx/xx/xxxx | Autor(es):                                      |      --
--                            | Descricao: Correção das linhas de CREATE TABLE  |      --
-- --------------------------------------------------------------------------------------
-- TABELA: Item
CREATE TABLE Item (
    id_item VARCHAR(8) PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(255),
    item_tipo VARCHAR(100) NOT NULL
);

-- TABELA: Instancia_de_Item
CREATE TABLE Instancia_de_Item (
    id_instanciaItem VARCHAR(8) PRIMARY KEY,
    id_item VARCHAR(8),
    FOREIGN KEY (id_item) REFERENCES Item(id_item)
);

-- TABELA: Inventario
CREATE TABLE Inventario (
    id_inventario VARCHAR(8) PRIMARY KEY,
    id_instanciaitem VARCHAR(8) NOT NULL,
    FOREIGN KEY (id_instanciaitem) REFERENCES Instancia_de_Item(id_instanciaItem)
);

-- TABELA: Afinidade
CREATE TABLE Afinidade (
    id_afinidade VARCHAR(8) PRIMARY KEY,
    tipo_afinidade VARCHAR(8) NOT NULL,
    xp_atual INTEGER NOT NULL,
    xp_max INTEGER NOT NULL,
    nivel_atual INTEGER NOT NULL
);

-- TABELA: Habilidades
CREATE TABLE Habilidades (
    id_habilidade VARCHAR(8) PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    tipo_habilidade VARCHAR(6) NOT NULL,
    nivel INT NOT NULL,
    afinidadeTipo VARCHAR(15) NOT NULL,
    coolDown INTEGER NOT NULL,
    desbloqueado BOOLEAN NOT NULL
);

-- TABELA: Campus
CREATE TABLE Campus (
    id_campus VARCHAR(8) PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(225) NOT NULL
);

-- TABELA: Setor
CREATE TABLE Setor (
    id_setor VARCHAR(8) PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(225) NOT NULL,
    id_proxSetor VARCHAR(8),
    id_prevSetor VARCHAR(8),
    id_campus VARCHAR(8) NOT NULL,
    FOREIGN KEY (id_proxSetor) REFERENCES Setor(id_setor),
    FOREIGN KEY (id_prevSetor) REFERENCES Setor(id_setor),
    FOREIGN KEY (id_campus) REFERENCES Campus(id_campus)
	-- outra forma id_proxSetor VARCHAR(8) NOT NULL REFERENCES Setor(id_setor),
);

-- TABELA: Sala_Comum
CREATE TABLE Sala_Comum (
    id_sala VARCHAR(8) PRIMARY KEY,
    id_instanciaItem VARCHAR(8) NOT NULL,
    id_setor VARCHAR(8) NOT NULL,
    descricao VARCHAR(255) NOT NULL,
    FOREIGN KEY (id_instanciaItem) REFERENCES Instancia_de_Item(id_instanciaItem),
    FOREIGN KEY (id_setor) REFERENCES Setor(id_setor)
);

-- TABELA: Estudante
CREATE TABLE Estudante (
    id_estudante VARCHAR(8) PRIMARY KEY,
    id_inventario VARCHAR(8) NOT NULL,
    id_habilidade VARCHAR(8) NOT NULL,
    id_afinidade VARCHAR(8) NOT NULL,
    id_sala VARCHAR(8) NOT NULL,
    nome VARCHAR(100) NOT NULL,
    vida INTEGER NOT NULL,
    estresse INTEGER NOT NULL,
    total_moedas INTEGER NOT NULL,
    FOREIGN KEY (id_inventario) REFERENCES Inventario(id_inventario),
    FOREIGN KEY (id_habilidade) REFERENCES Habilidades(id_habilidade),
    FOREIGN KEY (id_afinidade) REFERENCES Afinidade(id_afinidade),
    FOREIGN KEY (id_sala) REFERENCES Sala_Comum(id_sala)
);

-- TABELA: Dungeon_Academica
CREATE TABLE Dungeon_Academica (
    id_dungeon VARCHAR(8) PRIMARY KEY,
    id_sala VARCHAR(8) NOT NULL,
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(225) NOT NULL,
    FOREIGN KEY (id_sala) REFERENCES Sala_Comum(id_sala)
);

-- TABELA: Gabinete_Boss
CREATE TABLE Gabinete_Boss (
    id_gabinete_boss VARCHAR(8) PRIMARY KEY,
    id_dungeon VARCHAR(8) NOT NULL,
    FOREIGN KEY (id_dungeon) REFERENCES Dungeon_Academica(id_dungeon)
);

-- TABELA: Boss
CREATE TABLE Boss (
    id_boss VARCHAR(8) PRIMARY KEY,
    vida INTEGER NOT NULL,
    id_gabinete_boss VARCHAR(8) NOT NULL,
    nome VARCHAR(100) NOT NULL,
    id_habilidade VARCHAR(8) NOT NULL,
    FOREIGN KEY (id_gabinete_boss) REFERENCES Gabinete_Boss(id_gabinete_boss),
    FOREIGN KEY (id_habilidade) REFERENCES Habilidades(id_habilidade)
);

-- TABELAS DE AÇÃO
CREATE TABLE Ataque (
    danoCausado INTEGER NOT NULL,
    porcentagemAcerto FLOAT NOT NULL
);

CREATE TABLE Cura (
    vidaRecuperada INTEGER NOT NULL
);

CREATE TABLE Defesa (
    danoMitigado INTEGER NOT NULL
);

-- TABELA: Loja
CREATE TABLE Loja (
    id_loja VARCHAR(8) PRIMARY KEY NOT NULL,
    nome VARCHAR(255) NOT NULL,
    id_habilidade VARCHAR(8),
    id_instanciaItem VARCHAR(8),
    id_sala VARCHAR(8) NOT NULL,
    FOREIGN KEY (id_habilidade) REFERENCES Habilidades(id_habilidade),
    FOREIGN KEY (id_instanciaItem) REFERENCES Instancia_de_Item(id_instanciaItem),
    FOREIGN KEY (id_sala) REFERENCES Sala_Comum(id_sala)
);

-- TABELAS DE ITENS
CREATE TABLE Reliquia (
    id_reliquia VARCHAR(8) PRIMARY KEY,
    tipo_reliquia VARCHAR(100) NOT NULL
);

CREATE TABLE Consumivel (
    efeito INTEGER NOT NULL,
    preco FLOAT NOT NULL
);

CREATE TABLE Equipavel (
    efeito INTEGER NOT NULL,
    preco INTEGER NOT NULL,
    equipado BOOLEAN NOT NULL
);

-- TABELA: Monstro e Instancia
CREATE TABLE Montro (
    id_monstro VARCHAR(8) PRIMARY KEY,
    id_habilidade VARCHAR(8),
    vida_max INTEGER NOT NULL,
    tipo_setor VARCHAR(100) NOT NULL,
    nome VARCHAR(100) NOT NULL,
    FOREIGN KEY (id_habilidade) REFERENCES Habilidades(id_habilidade)
);

CREATE TABLE Instancia_de_Monstro (
    id_instanciaMonstro VARCHAR(8) PRIMARY KEY,
    id_monstro VARCHAR(8) NOT NULL,
    id_dungeon VARCHAR(8) NOT NULL,
    vida_atual INTEGER NOT NULL,
    FOREIGN KEY (id_monstro) REFERENCES Montro(id_monstro),
    FOREIGN KEY (id_dungeon) REFERENCES Dungeon_Academica(id_dungeon)
);

-- TABELA: Batalha
CREATE TABLE Batalha (
    id_batalha VARCHAR(8) PRIMARY KEY,
    id_instanciaMonstro VARCHAR(8) NOT NULL,
    player_win BOOLEAN NOT NULL,
    Moedas INTEGER NOT NULL,
    estresse_gasto INTEGER NOT NULL,
    xp_area INTEGER NOT NULL,
    FOREIGN KEY (id_instanciaMonstro) REFERENCES Instancia_de_Monstro(id_instanciaMonstro)
);

-- TABELA: Duelo
CREATE TABLE Duelo (
    id_duelo VARCHAR(8) PRIMARY KEY,
    id_reliquia VARCHAR(8) NOT NULL,
    id_boss VARCHAR(8) NOT NULL,
    player_win BOOLEAN NOT NULL,
    Moedas INTEGER NOT NULL,
    estresse_gasto INTEGER NOT NULL,
    FOREIGN KEY (id_reliquia) REFERENCES Reliquia(id_reliquia),
    FOREIGN KEY (id_boss) REFERENCES Boss(id_boss)
);
