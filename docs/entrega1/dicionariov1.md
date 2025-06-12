# DD - Dicionário de Dados

De acordo com a *UC Merced Library*,
> "Um Dicionário de Dados é uma coleção de nomes, definições e atributos sobre elementos de dados que estão sendo usados ​​ou capturados em um banco de dados, sistema de informação ou parte de um projeto de pesquisa. Ele descreve os significados e propósitos dos elementos de dados dentro do contexto de um projeto e fornece orientações sobre interpretação, significados aceitos e representação. [...]. Os metadados incluídos em um Dicionário de Dados podem auxiliar na definição do escopo e das características dos elementos de dados, bem como nas regras para seu uso e aplicação. "

## Entidade: Campus

**Descrição:** A entidade Campus descreve os campus presentes no jogo e outras informações, como: seu número de identificação e nome.

| Nome      | Descrição                         | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| --------- | --------------------------------- | ------------ | ------- | ------------------------------------------------------------------ |
| id_campus | Identificador único do campus     | Inteiro      |         | - PK<br>- Not Null<br>                                             |
| nome      | Nome do campus                    | varchar      | 100     | - Not Null                                                         |
| descricao | Descrição do campus               | varchar      | 255     | - Not Null                                                         |

## Entidade: Dungeon\_Academica

**Descrição:** A entidade `Dungeon_Academica` descreve Dungeons que se relacionam a salas comuns no jogo e outras informações, como: seu número de identificação, nome, descrição e id do tema. Representa desafios ou ambientes acadêmicos temáticos que fazem parte do sistema. Cada dungeon está relacionada a um tema específico de aprendizado, e contém informações como nome e descrição do desafio.


| Nome       | Descrição                                            | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ---------- | ---------------------------------------------------- | ------------ | ------- | ------------------------------------------------------------------ |
| id_dungeon | Identificador da Dungeon | inteiro  || - FK<br>- PK<br>- Not Null|
| nome       | Nome da Dungeon Acadêmica   | varchar      | 100     | - Not Null |
| descricao  | Descrição da Dungeon Acadêmica   | varchar      | 255     | - Not Null|
| id_tema | Identificador do Tema | inteiro  || - PK<br>- Not Null|

## Entidade: Boss

**Descrição**: A tabela Boss representa criaturas especiais (chefes) dentro do sistema, associando cada uma a uma relíquia que pode ser guardada, protegida ou concedida ao ser derrotado. Cada boss é uma criatura registrada previamente e está relacionado a uma relíquia específica. A tabela é uma especialização da entidade `Criatura`. Herda todos os atributos de `Criatura`


| Nome             | Descrição                                           | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ---------------- | --------------------------------------------------- | ------------ | ------- | ------------------------------------------------------------------ |
| id_boss  | Identificador do Boss  | inteiro| | - PK<br>- FK<br>- Not Null                                         |
| id_reliquia    | Identificador da(s) habilidade(s) que o boss possui |inteiro|      | - FK<br>- Not Null                                                 |


## Entidade: Instancia_de_Criatura

**Descrição**: A tabela Instancia de Criatura registra cada aparição individual de uma criatura dentro de uma dungeon. Serve para controlar dinamicamente a vida atual da criatura durante interações ou combates em ambientes específicos do jogo.

| Nome             | Descrição                                       | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ---------------- | ----------------------------------------------- | ------------ | ------- | ------------------------------------------------------------------ |
| id_instanciaMonstro | Identificador do monstro      | inteiro      |   | - PK<br>- Not Null                                                 |
| id_criatura       | Identificador da criatura |inteiro     |      | - FK<br>- Not Null                                                 |
| vida_atual | Vida atual da criatura | inteiro      |      | - Not Null                                                 |
| id_dungeon       | Identificador da Dungeon | inteiro   |     | - FK<br>- Not Null                                                 |

## Entidade: Ataque

**Descrição:** A entidade `Ataque` descreve o tipo de ataque, que está ligado a uma habilidade. Possui informações, como dano causado e porcentagem de acerto e herda todos os atributos de habilidade.

| Nome              | Descrição                                | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ----------------- | ---------------------------------------- | ------------ | ------- | ------------------------------------------------------------------ |
| danoCausado       | Indica o dano causado pelo ataque        | inteiro |  | - Not Null|
| porcentagemAcerto | Indica a porcentagem de acerto do ataque | float |  | - Not Null|    
| id_habilidade | Identificador de habilidade | inteiro |  | - PK<br>- FK<br>- Not Null|      


## Entidade: Cura

**Descrição:** A entidade `Cura` descreve o tipo de cura, que está ligado a uma habilidade. Possui informação de vida recuperada e herda todos os atributos de habilidade.

| Nome           | Descrição                                                               | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| -------------- | ----------------------------------------------------------------------- | ------------ | ------- | ------------------------------------------------------------------ |
| vidaRecuperada | Indica o tanto de vida recuperada possibilitado pela habilidade de cura | int          |         | - Not Null |
| id_habilidade | Identificador de habilidade | inteiro |  | - PK<br>- FK<br>- Not Null|


## Entidade: Defesa

**Descrição:** A entidade `Defesa` descreve o tipo de defesa, que está ligado a uma habilidade. Possui informação de dano mitigado e herda todos os atributos de habilidade.

| Nome         | Descrição                                                 | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ------------ | --------------------------------------------------------- | ------------ | ------- | ------------------------------------------------------------------ |
| danoMitigado | Indica o tanto de dano mitigado possibilitado pela defesa | int          |         | - Not Null                                                         |
| id_habilidade | Identificador de habilidade | inteiro |  | - PK<br>- FK<br>- Not Null|      

## Entidade: Setor

**Descrição:** A entidade `Setor` descreve um setor que está dentro do campus. A chave primária composta indica que o mesmo id_setor poderia existir em mais de um campus, mas com distinção pelo id_campus. Possui informação de nome, descrição, identificador do campus, e duas chaves estrangeiras referenciando outras lomocomoções para acesso de outros setores, na qual, possui um auto-relacionamento em que a partir de um setor pode se chegar a outro, ou seja, esse relacionamento estre os setrores cria um tipo de estrutura de lista duplamente ligada. Essa estrutura pode ser útil para organizar setores em ordem (por exemplo, geográfica ou lógica). Os campos id_prevSetor e id_proxSetor são auto-relacionamentos com a mesma tabela, ideais para navegação sequencial entre setores.

| Nome         | Descrição                                  | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ------------ | ------------------------------------------ | ------------ | ------- | ------------------------------------------------------------------ |
| id_setor     | Identificador do Setor                     | inteiro      |         | - PK<br>- Not Null                                                |
| id_campus    | Identificador do Campus                    | inteiro      |         | - PK<br>- FK<br>- Not Null                                        |
| nome         | Nome do Setor                              | varchar      | 100     | - Not Null                                                         |
| descricao    | Descrição do Setor                         | varchar      | 255     | - Not Null                                                         |
| id_proxSetor | Identificador do próximo setor(auto-relacion.) | inteiro      |        | - FK<br>- Not Null                                              |
| id_prevSetor | Identificador do setor anterior            | inteiro      |       | - FK<br>- Not Null                                                 |

## Entidade: Itens_Loja

**Descrição**: A tabela Itens Loja representa a relação entre as lojas disponíveis no sistema e os itens que estão à venda em cada uma delas. Essa tabela é usada para modelar o relacionamento muitos-para-muitos entre Loja e Item, indicando quais itens estão disponíveis em quais lojas.


| Nome | Descrição | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ---- | --------- | ------------ | ------- | ------------------------------------------------------------------ |
|id_loja|Identificador da loja|inteiro||- FK<br>- PK<br>- Not Null|
|id_item|Identificador de item|inteito||- PK<br>- FK<br>- Not Null|

## Entidade: Item

**Descrição**: A tabela `item` armazena os dados básicos de todos os itens disponíveis no sistema. Cada item possui uma descrição, um nome e um tipo que indica sua funcionalidade ou categoria.


| Nome      | Descrição             | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| --------- | --------------------- | ------------ | ------- | ------------------------------------------------------------------ |
| id_item   | Identificador do item | inteiro     |       | - PK<br>- Not Null                                                 |
| nome      | Nome do item          | varchar      | 100     | - Not Null                                                         |
| descricao | Descreve o item       | varchar      | 255     |                                                                    |
| item_tipo | Indica o tipo do item | varchar      | 100     | - Not Null                                                         |

## Entidade: Reliquia

**Descrição**: A tabela reliquia armazena os dados das relíquias disponíveis no sistema, que estão associadas a chefes (bosses) e possuem um tipo específico. Cada relíquia possui um identificador único e um tipo definido. É um tipo de item.

| Nome          | Descrição                   | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ------------- | --------------------------- | ------------ | ------- | ------------------------------------------------------------------ |
| id_reliquia   | Identificador da relíquia   | inteiro      |        | - PK<br>- Not Null                                                 |
| tipo | Descreve o tipo da relíquia | varchar      | 100     | - Not Null                                                         |

## Entidade: Consumivel

**Descrição:** A entidade `Consumível` descreve um item consumível. Herda todos os atributos de Item e possui informações como efeito e preço.

| Nome   | Descrição                             | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ------ | ------------------------------------- | ------------ | ------- | ------------------------------------------------------------------ |
| id_item | Identificador do item | int          |         | - PK<br>- FK<br>- Not Null                                                         |
| efeito  | Efeito do item              | float        |         | - Not Null                                                         |
| preco  | Preço do item consumível              | float        |         | - Not Null                                                         |

## Entidade: Equipavel

**Descrição:** A entidade `Equipavel` descreve um item equipável. Herda todos os atributos de Item e possui informações como efeito, preço e se está equipado ou não.

| Nome | Descrição | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ---- | --------- | ------------ | ------- | ------------------------------------------------------------------ |
|id_item|Identificador do item|int||- FK<br>- PK<br>- Not Null|
|efeito|Efeito causado por um item consumível|int||-Not Null|
|preco|O valor do item equipavel|int||-Not Null|
|equipado|indica se o item equipavel está equipado ou não |boolean|1 bit|-Not Null|

## Entidade: Monetario

**Descrição:** A tabela `monetario` representa itens do tipo monetário no sistema, como moedas ou valores que podem ser acumulados pelos jogadores. Essa tabela especializa a tabela item e define o valor numérico associado a esse tipo de recurso. Herda todos os atributos de Item.

| Nome | Descrição | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ---- | --------- | ------------ | ------- | ------------------------------------------------------------------ |
|id_item|Identificador do item|int||- FK<br>- PK<br>- Not Null|
|valor|O valor do item equipavel|int||-Not Null|

## Entidade: Sala_comum

**Descrição:** A tabela Sala_Comum representa as salas que compõem um setor dentro da estrutura do sistema. Cada sala está vinculada a um setor (id_setor) e possui um identificador próprio (id_sala). A estrutura permite o encadeamento de salas por meio de relacionamentos de anterior e próxima (id_prevSala e id_proxSala), formando uma sequência navegável. Além disso, cada sala pode conter funcionalidades específicas como loja (tem_loja) e dungeon (tem_dungeon), representadas por campos booleanos. Essa modelagem permite a navegação sequencial entre salas e a definição de pontos especiais dentro de um setor.

| Nome | Descrição | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ---- | --------- | ------------ | ------- | ------------------------------------------------------------------ |
|id_sala|Identificador único da sala|inteiro|  |- PK<br>- Not Null<br>|
|id_setor|Identificador único da sala|inteiro|  |- PK<br>- FK<br>- Not Null<br>|
|id_prevSala|Identificador da sala anterior|inteiro||- FK<br>- Not Null<br>|
|id_proxSala|Identificador da próxima sala|inteiro||- FK<br>- Not Null<br>|
|descrição|Descrição do que tem/contem na sala|varchar|255|-Not Null|
|nome | nome da sala|varchar|100|- Not Null|
|tem_loja|Se a sala possui loja|boolean| 1 bit |- Not Null<br>|
|tem_dungeon|Se a sala possui dungeon|boolean| 1 bit |- Not Null<br>|

## Entidade: Habilidade_Criatura

**Descrição:** Cada registro da tabela Habilidade_Criatura indica que uma determinada criatura possui uma determinada habilidade.

| Nome | Descrição | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ---- | --------- | ------------ | ------- | ------------------------------------------------------------------ |
|id_Criatura|Identificador da criatura|inteiro||- PK<br>- FK<br>- Not Null<br>|
|id_habilidade|Identificador da habilidade|inteiro||- PK<br>- FK<br>- Not Null<br>|

## Entidade: Habilidade_Estudante

**Descrição:** A tabela Habilidade_Estudante indica quais habilidades cada estudante possui, permitindo que cada estudante possa ter diversas habilidades cadastradas.

| Nome | Descrição | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ---- | --------- | ------------ | ------- | ------------------------------------------------------------------ |
|id_estudante|Identificador do estudante|inteiro||- PK<br>- FK<br>- Not Null<br>|
|id_habilidade|Identificador da habilidade|inteiro||- PK<br>- FK<br>- Not Null<br>|

## Entidade: Habilidade_Loja

**Descrição:** A tabela Habilidade_Loja representa o relacionamento entre lojas e habilidades disponíveis para venda. Ela define quais habilidades podem ser adquiridas nas lojas.

| Nome | Descrição | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ---- | --------- | ------------ | ------- | ------------------------------------------------------------------ |
|id_loja|Identificador da loja|inteiro||- PK<br>- FK<br>- Not Null<br>|
|id_habilidade|Identificador da habilidade|inteiro||- PK<br>- FK<br>- Not Null<br>|


## Entidade: Instancia_de_item

**Descrição:** Armazena as instâncias de itens que existem no sistema, associando cada item a uma sala e/ou a um estudante. Cada instância possui um identificador próprio e referencia um tipo de item. Esta tabela permite controlar a posse e localização dos itens no ambiente.

| Nome | Descrição | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ---- | --------- | ------------ | ------- | ------------------------------------------------------------------ |
|id_instanciaitem|Identificador da instância do item|inteiro||- PK<br>- Not Null<br>|
|id_item|Identificador do item que foi instânciado|inteiro||- PK<br>- FK<br>- Not Null<br>|
|id_sala|Identificador da sala|inteiro||- FK<br>- Not Null<br>|
|id_estudante|Identificador do estudante|inteiro||- FK<br>- Not Null<br>|

## Entidade: Estudante

**Descrição:** A tabela Estudante armazena os dados principais dos estudantes que participam do sistema. Cada estudante possui atributos como vida, estresse e total de dinheiro acumulado. Essa tabela também indica a qual sala o estudante pertence, por meio de uma chave estrangeira.

| Nome | Descrição | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ---- | --------- | ------------ | ------- | ------------------------------------------------------------------ |
|id_estudande|Identificador de estudante|inteiro||- PK<br>- Not Null<br>|
|id_sala|Identificador da sala que o estudante está|inteiro||- FK<br>- Not Null<br>|
|nome|Nome do usuário|varchar|100|-Not Null|
|vida|Total de vida que o estudante tem|int||-Not Null|
|estresse|o Nível de stress que o usuário está|int||-Not Null|
|total_dinheiro|Total de moedas que o estudante tem|int||-Not Null|

## Entidade: monstroSimples

**Descrição:** A tabela monstroSimples representa criaturas do tipo simples (não-chefes) que aparecem no jogo. Esses monstros, ao serem derrotados, concedem uma certa quantidade de experiência temática (XP) ao jogador e podem deixar moedas como recompensa. A tabela é uma especialização da entidade `Criatura`. Herda todos os atributos de `Criatura`

| Nome | Descrição | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ---- | --------- | ------------ | ------- | ------------------------------------------------------------------ |
|id_criatura|Identificador da criatura|inteiro||- PK<br>- FK<br>- Not Null<br>|
|xp_tema|Quanidade de pontos que o tema oferece para determinada criatura|inteiro||- Not Null<br>|
|qtd_moedas|Quantidades de moedas que o monstro dropa|int||-Not Null|

  ## Entidade: Criatura 

**Descrição:** A tabela Criatura armazena os dados básicos de todas as criaturas presentes no sistema, sejam elas monstros simples ou bosses. Cada criatura possui atributos como nível, vida máxima, tipo e uma descrição que pode ser usada para fins narrativos ou funcionais no jogo.

| Nome | Descrição | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ---- | --------- | ------------ | ------- | ------------------------------------------------------------------ |
|id_criatura| Identificador da criatura|inteiro||- PK<br>- Not Null<br>|
|nivel|Nivel da criatura|int|100|- FK<br>- Not Null<br>|
|tipo_criatura|Tipo da criatura|varchar|100|- Not Null<br>|
|vida_max|Valor da vida da criatura|int||-Not Null|
|nome|Nome da criatura|varchar|100|- Not Null<br>|
|descricao|Descriçao da criatura|varchar|200|-Not Nul|


## Entidade: Afinidade

**Descrição:** A tabela Afinidade armazena o relacionamento entre estudantes e temas, representando o nível de domínio que cada estudante possui sobre determinado tema. Cada registro representa uma afinidade única entre um estudante e um tema. Esta tabela possui chave primária composta e duas chaves estrangeiras, referenciando as tabelas Estudante e Tema.


| Nome | Descrição | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ---- | --------- | ------------ | ------- | ------------------------------------------------------------------ |
|id_afinidade|Identificador da afinidade|inteiro||- PK<br>- FK<br>- Not Null|
|id_tema|Identificador do tema |inteiro| |- PK<br>- FK<br>- Not Null|
|xp_atual|xp atual que a afinidade tem|inteiro||- Not Null|
|nivel_atual|Qual o nível atual da afinidade|inteiro||- Not Null|

## Entidade: Habilidades

**Descrição:** Esta entidade contém os dados das habilidades que uma criatura, estudante, tema e loja podem ter. Ela armazena todas as habilidades disponíveis no sistema. Cada habilidade possui um identificador único (id_habilidade), um nome, um nível associado (nivel) e um tempo de recarga (cooldown). As habilidades estão associadas a um Tema, por meio da chave estrangeira id_tema, e possuem uma classificação por tipo (tipo_habilidade). Essa tabela permite organizar as habilidades por complexidade, categoria e tema relacionado, sendo fundamental para o nosso sistema, que envolve a evolução de personagem, aprendizado progressivo e gamificação.

| Nome | Descrição | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ---- | --------- | ------------ | ------- | ------------------------------------------------------------------ |
|id_habilidade | Identificador Da habilidade|inteiro||- PK<br>- Not Null<br> |
|nome | nome da habilidade|varchar|100|- Not Null|
|tipo_habilidade|Qual o tipo da habilidade|varchar|10|- Not Null|
|nivel|Qual o nível da habilidade|inteiro||- Not Null|
|coolDown|tempo de recarga da habilidade|inteiro||- Not Null|
|id_tema|Identificador de Tema|inteiro||- PK<br>- Not Null|


## Entidade: Tema

**Descrição:** Contém as temáticas: Matemática, Programação, Engenharias, Gerais e Humanidades.

| Nome | Descrição | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ---- | --------- | ------------ | ------- | ------------------------------------------------------------------ |
|id_tema | Identificador do Tema|inteiro| |- PK<br>- Not Null<br> |
|nome | nome da habilidade |varchar|100|- Not Null|



## Histórico de Versões
| Versão |  Data  | Descrição| Autor                 |
| :----: | :--------: | ---------------------------------- | -------------------------------------------------------------------------------- |
| `1.0` | 01/05/2025 | Criação do Dicionário de Dados      | [Ludmila Nunes](https://github.com/ludmilaaysha) & [Isaque Camargos](https://github.com/isaqzin)|
| `2.0` | 10/06/2025 | Atualização do Dicionário de Dados      | [Milena Marques](https://github.com/milenamso)|
