# DD - Dicionário de Dados

De acordo com a *UC Merced Library*,
> "Um Dicionário de Dados é uma coleção de nomes, definições e atributos sobre elementos de dados que estão sendo usados ​​ou capturados em um banco de dados, sistema de informação ou parte de um projeto de pesquisa. Ele descreve os significados e propósitos dos elementos de dados dentro do contexto de um projeto e fornece orientações sobre interpretação, significados aceitos e representação. [...]. Os metadados incluídos em um Dicionário de Dados podem auxiliar na definição do escopo e das características dos elementos de dados, bem como nas regras para seu uso e aplicação. "

## Entidade: Campus

**Descrição:** A entidade Campus descreve os campus presentes no jogo e outras informações, como: seu número de identificação e nome.

Observação: Essa tabela é chave estrangeira de `Setor`.

| Nome      | Descrição                         | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| --------- | --------------------------------- | ------------ | ------- | ------------------------------------------------------------------ |
| id_campus | Identificador da instância Campus | varchar      | 8       | - PK<br>- Not Null<br>                                             |
| nome      | Nome do campus                    | varchar      | 100     | - Not Null                                                         |
| descricao | Descrição do campus               | varchar      | 255     | - Not Null                                                         |


## Entidade: Dungeon\_Academica

**Descrição:** A entidade `Dungeon_Academica` descreve Dungeons que se relacionam a salas comuns no jogo e outras informações, como: seu número de identificação, id da sala a que se relaciona, nome, descrição e tipo de afinidade.

**Observação:** Essa tabela possui chave estrangeira da entidade `Sala_Comum`.

| Nome       | Descrição                                            | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ---------- | ---------------------------------------------------- | ------------ | ------- | ------------------------------------------------------------------ |
| id_dungeon | Identificador da Dungeon                             | varchar      | 8       | - PK<br>- Not Null                                                 |
| id_sala    | Identificador da sala em que a Dungeon está presente | varchar      | 8       | - FK<br>- Not Null                                                 |
| nome       | Nome da Dungeon Acadêmica                            | varchar      | 100     | - Not Null                                                         |
| descricao  | Descrição da Dungeon Acadêmica                       | varchar      | 255     | - Not Null                                                         |

## Entidade: Boss

**Descrição**: A entidade `Boss` descreve o Boss de um Gabinete, que está presente em uma Sala_Comum no jogo, e outras informações, como: seu número de identificação, id do gabinete a que se relaciona, nome, descrição e tipo de afinidade.

**Observação**: Essa tabela possui chaves estrangeiras das entidades `Gabinete_Boss` e `Habilidades`.

| Nome             | Descrição                                           | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ---------------- | --------------------------------------------------- | ------------ | ------- | ------------------------------------------------------------------ |
| id_boss          | Identificador do Boss                               | varchar      | 8       | - PK<br>- Not Null                                                 |
| vida             | Quantidade de vida que o boss possui no momento     | int          |         | - Not Null                                                         |
| id_gabinete_boss | Identificador do gabinete em que o Boss fica        | varchar      | 8       | - FK<br>- Not Null                                                 |
| nome             | Nome do Boss                                        | varchar      | 100     | - Not Null                                                         |
| id_habilidade    | Identificador da(s) habilidade(s) que o boss possui | varchar      | 8       | - FK<br>- Not Null                                                 |
| id_habilidade    | Identificador da(s) habilidade(s) que o boss possui | varchar      | 8       | - Not Null                                                         |

## Entidade: Gabinete_Boss

**Descrição**: A entidade `Gabinete_Boss` descreve o Gabinete de um Boss, presente em alguma Dungeon no jogo. Possui informações, como: seu número de identificação e identificação da Dungeon em que está.

**Observação**: Essa tabela possui chave estrangeira da entidade `Dungeon_Academica`.

| Nome             | Descrição                                       | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ---------------- | ----------------------------------------------- | ------------ | ------- | ------------------------------------------------------------------ |
| id_gabinete_boss | Identificador do gabinete do Boss               | varchar      | 8       | - PK<br>- Not Null                                                 |
| id_dungeon       | Identificador da Dungeon em que o gabinete está | varchar      | 8       | - FK<br>- Not Null                                                 |


## Entidade: Ataque

**Descrição:** A entidade `Ataque` descreve o tipo de ataque, que está ligado a uma habilidade. Possui informações, como dano causado e porcentagem de acerto e herda todos os atributos de habilidade.

**Observação:**** Essa tabela não possui chave estrangeira.

<!-- 🔔 **Nota:** Verificar se esse é realmente o relacionamento correto. -->


| Nome              | Descrição                                | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ----------------- | ---------------------------------------- | ------------ | ------- | ------------------------------------------------------------------ |
| danoCausado       | Indica o dano causado pelo ataque        | int          |         | - Not Null                                                         |
| porcentagemAcerto | Indica a porcentagem de acerto do ataque | float        |         | - Not Null                                                         |

## Entidade: Cura

**Descrição:** A entidade `Cura` descreve o tipo de cura, que está ligado a uma habilidade. Possui informação de vida recuperada e herda todos os atributos de habilidade.

**Observação:**** Essa tabela não possui chave estrangeira.

<!-- 🔔 **Nota:** Verificar se esse é realmente o relacionamento correto. -->

| Nome           | Descrição                                                               | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| -------------- | ----------------------------------------------------------------------- | ------------ | ------- | ------------------------------------------------------------------ |
| vidaRecuperada | Indica o tanto de vida recuperada possibilitado pela habilidade de cura | int          |         | - Not Null                                                         |


## Entidade: Defesa

**Descrição:** A entidade `Defesa` descreve o tipo de defesa, que está ligado a uma habilidade. Possui informação de dano mitigado e herda todos os atributos de habilidade.

**Observação:**** Essa tabela não possui chave estrangeira.

<!-- 🔔 **Nota:** Verificar se esse é realmente o relacionamento correto. -->

| Nome         | Descrição                                                 | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ------------ | --------------------------------------------------------- | ------------ | ------- | ------------------------------------------------------------------ |
| danoMitigado | Indica o tanto de dano mitigado possibilitado pela defesa | int          |         | - Not Null                                                         |

## Entidade: Setor

**Descrição:** A entidade `Setor` descreve um setor que está dentro do campus. Possui informação de nome, descrição, identificador do campus em que está e possui um auto-relacionamento em que a partir de um setor pode se chegar a outro.

**Observação**: Essa tabela possui chaves estrangeiras das entidades `Setor` e `Campus`.

| Nome         | Descrição                                  | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ------------ | ------------------------------------------ | ------------ | ------- | ------------------------------------------------------------------ |
| id_setor     | Identificador do Setor                     | varchar      | 8       | - PK<br>- Not Null                                                 |
| nome         | Nome do Setor                              | varchar      | 100     | - Not Null                                                         |
| descricao    | Descrição do Setor                         | varchar      | 255     | - Not Null                                                         |
| id_proxSetor | Identificador do próximo setor             | varchar      | 8       | - PK<br>- FK         <br>- Not Null                                              |
| id_prevSetor | Identificador do setor anterior            | varchar      | 8       | - PK<br>- FK<br>- Not Null                                                       |
| id_campus    | Identificador do campus em que se encontra | varchar      | 8       | - FK<br>- Not Null                                                 |


## Entidade: Loja

**Descrição**: A entidade `Loja` descreve uma loja, que está dentro de uma sala, e por meio da qual podem ser compradas habilidades e instâncias de itens.

**Observação**: Essa tabela possui chaves estrangeiras das entidades `Habilidade`, `Instancia_de_item` e `Sala_Comum`.

| Nome             | Descrição                                                   | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ---------------- | ----------------------------------------------------------- | ------------ | ------- | ------------------------------------------------------------------ |
| id_loja          | Identificador da Loja                                       | varchar      | 8       | - PK<br>- Not Null                                                 |
| nome             | Nome da loja                                                | varchar      | 255     | - Not Null                                                         |
| id_habilidade    | Identificador da habilidade que está à venda na loja        | varchar      | 8       | - FK                                                               |
| id_instanciaItem | Identificador da instância de item que está à venda na loja | varchar      | 8       | - FK<br>- Not Null                                                 |
| id_sala          | Identificador da sala em que a loja está                    | varchar      | 8       | - FK<br>- Not Null                                                 |

## Entidade: Item

**Descrição**: A entidade `Item` descreve um tipo de item, que possui informações de tipo, descrição, nome e identificador.

**Observação**: Essa tabela não possui chave estrangeira, mas é chave estrangeira da entidade `Instância_de_item`.

| Nome      | Descrição             | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| --------- | --------------------- | ------------ | ------- | ------------------------------------------------------------------ |
| id_item   | Identificador do item | varchar      | 8       | - PK<br>- Not Null                                                 |
| nome      | Nome do item          | varchar      | 100     | - Not Null                                                         |
| descricao | Descreve o item       | varchar      | 255     |                                                                    |
| item_tipo | Indica o tipo do item | varchar      | 100     | - Not Null                                                         |

## Entidade: Relíquia

**Descrição**: A entidade `Relíquia` descreve uma relíquia, que é um tipo de item. Se relaciona a um duelo sendo chave estrangeira dele. Herda todos os atributos de Item.

Observação: Essa tabela é chave estrangeira da entidade `Duelo`.

| Nome          | Descrição                   | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ------------- | --------------------------- | ------------ | ------- | ------------------------------------------------------------------ |
| id_reliquia   | Identificador da relíquia   | varchar      | 8       | - PK<br>- Not Null                                                 |
| tipo_reliquia | Descreve o tipo da relíquia | varchar      | 100     | - Not Null                                                         |

## Entidade: Consumível

**Descrição:** A entidade `Consumível` descreve um item consumível. Herda todos os atributos de Item e possui informações como efeito e preço.

**Observação:** Essa tabela não possui chave estrangeira da entidade.

| Nome   | Descrição                             | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ------ | ------------------------------------- | ------------ | ------- | ------------------------------------------------------------------ |
| efeito | Efeito causado por um item consumível | int          |         | - Not Null                                                         |
| preco  | Preço do item consumível              | float        |         | - Not Null                                                         |

## Entidade: Equipável

**Descrição:** A entidade `Equipavel` descreve um item equipável. Herda todos os atributos de Item e possui informações como efeito, preço e se está equipado ou não.

**Observação:** Essa tabela não possui chave estrangeira.

| Nome | Descrição | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ---- | --------- | ------------ | ------- | ------------------------------------------------------------------ |
|efeito|Efeito causado por um item consumível|int||-Not Null|
|preco|O valor do item equipavel|int||-Not Null|
|equipado|indica se o item equipavel está equipado ou não |boolean||-Not Null|

## Entidade: Sala comum

**Descrição:** É a entidade que representa as salas em que o estudante irá andar.

**Observação:** Essa tabela possui chave estrangeira da entidade `setor` e `instancia_de_item` e as entidades `setor`, `loja`, `estudante` e `Dungeon_Academica` possuem chave estrangeira dessa entidade.

| Nome | Descrição | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ---- | --------- | ------------ | ------- | ------------------------------------------------------------------ |
|id_sala|Identificador da sala|varchar|8|- PK<br>- Not Null<br>|
|id_instanciaitem|Identificador da instância do item que a sala contem|varchar|8|- FK<br>- Not Null<br>|
|id_setor|Identificador do setor em que a sala está|varchar|8|- FK<br>- Not Null<br>|
|descrição|Descrição do que tem/contem na sala|varchar|255|-Not Null|
|nome | nome da sala|varchar|100|- Not Null|

## Entidade: Inventário

**Descrição:** Entidade que contem as instâncias de item que o estudante carrega com si.

**Observação:** Essa tabela possui chave estrangeira da entidade `instancia_de_item` e a entidade `estudante` tem chave estrangeira dessa entidade.

| Nome | Descrição | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ---- | --------- | ------------ | ------- | ------------------------------------------------------------------ |
|id_inventário|Identificador do inventário|varchar|8|- PK<br>- Not Null<br>|
|id_instanciaitem|Identificador da instância do item que o inventário armazena|varchar|8|- FK<br>- Not Null<br>|


## Entidade: Instância de item

**Descrição:** É a instância do item.

**Observação:** Essa tabela possui chave estrangeira da entidade `item` e as entidades `loja`, `inventario` e `sala_comum` possuem chave estrangeira desta entidade.

| Nome | Descrição | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ---- | --------- | ------------ | ------- | ------------------------------------------------------------------ |
|id_instanciaitem|Identificador da instância do item|varchar|8|- PK<br>- Not Null<br>|
|id_item|Identificador do item que foi instânciado|varchar|8|- FK<br>- Not Null<br>|

## Entidade: Batalha

**Descrição:** É a entidade que representa uma agregação do relacionamento entre Instância de monstro e o estudante

**Observação:** Essa tabela possui chave estrangeira da entidade `instância de Monstro`.

| Nome | Descrição | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ---- | --------- | ------------ | ------- | ------------------------------------------------------------------ |
|id_batalha|Identificador da batalha|varchar|8|- PK<br>- Not Null<br>|
|id_instânciaMonstro|Identificador da instância monstro que participa da batalha|varchar|8|- FK<br>- Not Null<br>|
|player_win|Identifica se o estudante venceu ou não|boolean||-Not Null|
|Moedas|Quantas moedas o duelo gerou|int||-Not Null|
|estresse_gasto|Quanto de estresse o usuário gastou no duelo|int||-Not Null|
|xp_area|xp relacionado a area ganho na batalha|int||-Not Null|

## Entidade: Duelo

**Descrição:** É a entidade que representa uma agregação do relacionamento entre boss e o estudante

**Observação:** Essa tabela possui chave estrangeira da entidade `Reliquia` e `Boss`.

| Nome | Descrição | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ---- | --------- | ------------ | ------- | ------------------------------------------------------------------ |
|id_duelo|Identificador do duelo|varchar|8|- PK<br>- Not Null<br>|
|id_reliquia|Identificador da reliquia que o duelo vai dropar|varchar|8|- FK<br>- Not Null<br>|
|id_boss|Identificador do boss que duelou com o estudante|varchar|8|- FK<br>- Not Null<br>|
|player_win|Identifica se o estudante venceu ou não|boolean||-Not Null|
|Moedas|Quantas moedas o duelo gerou|int||-Not Null|
|estresse_gasto|Quanto de estresse o usuário gastou no duelo|int||-Not Null|

## Entidade: Estudante

**Descrição:** É a entidade estuande que o jogador controla no jogo, ele batalha, duela, evolui esta entidade.

**Observação:** Essa tabela possui chave estrangeira das entidades `sala`, `inventario`, `habilidade` e `afinidade`.

| Nome | Descrição | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ---- | --------- | ------------ | ------- | ------------------------------------------------------------------ |
|id_estudande|Identificador de estudante|varchar|8|- PK<br>- Not Null<br>|
|id_inventario|Identificador do inventário que o estudante tem|varchar|8|- FK<br>- Not Null<br>|
|id_habilidade|Identificador das habilidades que o estudante possui|varchar|8|- FK<br>- Not Null<br>|
|id_afinidade|Identificador das afinadades do estudante|varchar|8|- FK<br>- Not Null<br>|
|id_sala|Identificador da sala que o estudante está|varchar|8|- FK<br>- Not Null<br>|
|nome|Nome do usuário|varchar|100|-Not Null|
|vida|Total de vida que o estudante tem|int||-Not Null|
|estresse|o Nível de stress que o usuário está|int||-Not Null|
|total_moedas|Total de moedas que o estudante tem|int||-Not Null|

## Entidade: Monstro

**Descrição:** É a entidade monstro, o qual o estudante deve derrotar para obter moeda e XP.

**Observação:** Essa tabela possui chave estrangeira da entidade `Habilidade` e entidade `Instância de monstro` tem chave estrangeira desta entidade.

| Nome | Descrição | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ---- | --------- | ------------ | ------- | ------------------------------------------------------------------ |
|id_monstro|Identificador do monstro|varchar|8|- PK<br>- Not Null<br>|
|id_habilidade|Identificador das habilidades que um monstro pode ter|varchar|8|- FK<br>- Not Null<br>|
|vida_max|Vida máxima que o monstro pode ter|int||-Not Null|
|tipo_setor|Tipo do setor em que o monstro está presente |varchar|100|-Not Null|
|nome|Nome do monstro|varchar|100|-Not Null|

## Entidade: Instância de Monstro

**Descrição:** É a instância do monstro.

**Observação:** Essa tabela possui chave estrangeira da entidade `Dungeon_academia` e `Monstro`, a entidade `Batalha` tem chave estrangeira desta entidade.

| Nome | Descrição | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ---- | --------- | ------------ | ------- | ------------------------------------------------------------------ |
|id_instanciaMonstro| Identificador da instância de monstro|varchar|8|- PK<br>- Not Null<br>|
|id_monstro|Identificador do Monstro que foi instânciado|varchar|8|- FK<br>- Not Null<br>|
|id_Dungeon|Identificador da Dungeon que a instância está presente|varchar|8|- FK<br>- Not Null<br>|
|vida_atual|Valor da vida da instância do boss|int||-Not Null|


## Entidade: Afinidade

**Descrição:** Essa entidade contém os dados da afinidade que um estudante pode ter nas áreas de matemática, humanas, programação e gerais.

**Observação:** A tabela estudante tem chave estrageira desta entidade. 

| Nome | Descrição | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ---- | --------- | ------------ | ------- | ------------------------------------------------------------------ |
|id_afinidade|Identificador da afinidade|varchar|8|- PK<br>- Not Null<br>|
|tipo_afinidade|Tipo da afinidade, identifica a afinidade |varchar|8|- PK<br>- Not Null<br>|
|xp_atual|xp atual que a afinidade tem|int||- Not Null|
|xp_max|xp máximo para upar de nível|int||- Not Null|
|nivel_atual|Qual o nível atual da afinidade|int||- Not Null|

## Entidade: Habilidade

**Descrição:** Esta entidade contém os dados das habilidades que um monstro, boss ou estudante podem ter.

**Observação:** Essa entidade tem relação com outras três entidades as habilidades de ataque, defesa e cura, as entidades `loja`, `monstro`, `boss` e `estudante` tem chave estrangeira dessa entidade .

| Nome | Descrição | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ---- | --------- | ------------ | ------- | ------------------------------------------------------------------ |
|id_habilidade | Identificador Da habilidade|varchar|8|- PK<br>- Not Null<br> |
|nome | nome da habilidade|varchar|100|- Not Null|
|tipo_habilidade|Qual o tipo da habilidade|varchar|6|- Not Null|
|nivel|Qual o nível da habilidade|int||- Not Null|
|afinidadeTipo|Qual a afinidade da habilidade|varchar|15|- Not Null|
|coolDown|tempo de recarga da habilidade|int||- Not Null|
|desbloqueado|indica se a habilidade está desbloqueada ou não |boolean||- Not Null|



## Histórico de Versões
| Versão |  Data  | Descrição| Autor                 |
| :----: | :--------: | ---------------------------------- | -------------------------------------------------------------------------------- |
| `1.0` | 01/05/2025 | Criação do Dicionário de Dados      | [Ludmila Nunes](https://github.com/ludmilaaysha) & [Isaque Camargos](https://github.com/isaqzin)|