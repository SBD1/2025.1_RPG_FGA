# DD - Dicionário de Dados

De acordo com a *UC Merced Library*,
> "Um Dicionário de Dados é uma coleção de nomes, definições e atributos sobre elementos de dados que estão sendo usados ​​ou capturados em um banco de dados, sistema de informação ou parte de um projeto de pesquisa. Ele descreve os significados e propósitos dos elementos de dados dentro do contexto de um projeto e fornece orientações sobre interpretação, significados aceitos e representação. [...]. Os metadados incluídos em um Dicionário de Dados podem auxiliar na definição do escopo e das características dos elementos de dados, bem como nas regras para seu uso e aplicação."

<!-- ludmila alterou -->
## Entidade: campus

**Descrição:** A entidade Campus descreve os campus presentes no jogo e outras informações, como: seu número de identificação e nome.

| Nome      | Descrição                         | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| --------- | --------------------------------- | ------------ | ------- | ------------------------------------------------------------------ |
| id_campus | Identificador único do campus     | INT      |         | - PK<br>- Identity<br>                                             |
| nome      | Nome do campus                    | Char      | 100     | - Not Null                                                         |
| descricao | Descrição do campus               | Char      | 255     | - Not Null                                                         |

<!-- isaque alterou -->
## Entidade: dungeon\_Academica

**Descrição:** A entidade `Dungeon_Academica` descreve Dungeons que se relacionam a salas comuns no jogo e outras informações, como: seu número de identificação, nome, descrição e id do tema. Representa desafios ou ambientes acadêmicos temáticos que fazem parte do sistema. Cada dungeon está relacionada a um tema específico de aprendizado, e contém informações como nome e descrição do desafio.


| Nome       | Descrição                                            | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ---------- | ---------------------------------------------------- | ------------ | ------- | ------------------------------------------------------------------ |
| id_dungeon | Identificador da Dungeon | INT  || - FK<br>- PK<br>- Not Null|
| nome       | Nome da Dungeon Acadêmica   | Char      | 100     | - Not Null |
| descricao  | Descrição da Dungeon Acadêmica   | Char      | 255     | - Not Null|
| id_tema | Identificador do Tema | INT  || - FK<br>- Not Null|

<!-- ludmila alterou -->
## Entidade: boss

**Descrição**: A tabela boss representa criaturas especiais (chefes) dentro do sistema, associando cada uma a uma relíquia que pode ser guardada, protegida ou concedida ao ser derrotado. Cada boss é uma criatura registrada previamente e está relacionado a uma relíquia específica. A tabela é uma especialização da entidade `tipo_criatura`. Herda todos os atributos de `tipo_criatura`


| Nome             | Descrição                                           | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ---------------- | --------------------------------------------------- | ------------ | ------- | ------------------------------------------------------------------ |
| id_criatura  | Identificador do Boss  | INT | | - PK<br>- FK<br>- Not Null                                         |
| id_reliquia    | Identificador da(s) habilidade(s) que o boss possui |INT|      | - FK<br>- Not Null                                                 |
| nome    | Nome do boss | Char | 100     | - Not Null                                                 |
| descricao    | Descrição do boss |Char| 255     | - Not Null                                                 |
| nivel    | Nível associado ao boss |INT|      | - Not Null                                                 |
| vida_max    | Vida máxima que boss pode alcançar |INT|      | - Not Null                                                 |


<!-- ludmila alterou -->
## Entidade: instancia_de_criatura

**Descrição**: A tabela Instancia de Criatura registra cada aparição individual de uma criatura dentro de uma dungeon. Serve para controlar dinamicamente a vida atual da criatura durante interações ou combates em ambientes específicos do jogo.

| Nome             | Descrição                                       | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ---------------- | ----------------------------------------------- | ------------ | ------- | ------------------------------------------------------------------ |
| id_instanciaCriatura | Identificador da instância criatura     | INT      |   | - PK<br>- Not Null<br>- Identity                                                 |
| id_criatura       | Identificador da criatura |INT     |      | - FK<br>- Not Null                                                 |
| vida_atual | Vida atual da criatura | INT      |      | - Not Null                                                 |
| id_dungeon       | Identificador da Dungeon | INT   |     | - FK<br>- Not Null                                                 |

<!-- ludmila alterou -->
## Entidade: ataque

**Descrição:** A entidade `Ataque` descreve o tipo de ataque, que está ligado a uma habilidade. Possui informações, como dano causado e porcentagem de acerto e contém todos os atributos de habilidade.

| Nome              | Descrição                                | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ----------------- | ---------------------------------------- | ------------ | ------- | ------------------------------------------------------------------ |
| id_habilidade | Identificador de habilidade | INT |  | - PK<br>- FK<br>- Not Null|      
| id_tema | Identificador do tema ao qual habilidade está associada | INT |  | - PK<br>- FK<br>- Not Null|      
| nome | Nome da habilidade | Char | 100 | - Not Null|      
| nivel | Nível da habilidade | INT |  | - Not Null|      
| coolDown | Tempo de recarga | INT |  | - Not Null|    
| danoCausado       | Indica o dano causado pelo ataque        | INT |  | - Not Null|
|preco| Custo do ataque|INT||- Not Null|


<!-- ludmila alterou -->
## Entidade: cura

**Descrição:** A entidade `Cura` descreve o tipo de cura, que está ligado a uma habilidade. Possui informação de vida recuperada e herda todos os atributos de habilidade.

| Nome           | Descrição                                                               | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| -------------- | ----------------------------------------------------------------------- | ------------ | ------- | ------------------------------------------------------------------ |
| id_habilidade | Identificador de habilidade | INT |  | - PK<br>- FK<br>- Not Null|      
| id_tema | Identificador do tema ao qual habilidade está associada | INT |  | - PK<br>- FK<br>- Not Null|      
| nome | Nome da habilidade | Char | 100 | - Not Null|      
| nivel | Nível da habilidade | INT |  | - Not Null|      
| coolDown | Tempo de recarga | INT |  | - Not Null|   
| vidaRecuperada | Indica o tanto de vida recuperada possibilitado pela habilidade de cura | INT          |         | - Not Null |
|preco| Custo cura|INT||- Not Null|


<!-- ludmila alterou -->
## Entidade: defesa

**Descrição:** A entidade `Defesa` descreve o tipo de defesa, que está ligado a uma habilidade. Possui informação de dano mitigado e herda todos os atributos de habilidade.

| Nome         | Descrição                                                 | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ------------ | --------------------------------------------------------- | ------------ | ------- | ------------------------------------------------------------------ |
| id_habilidade | Identificador de habilidade | INT |  | - PK<br>- FK<br>- Not Null|      
| id_tema | Identificador do tema ao qual habilidade está associada | INT |  | - PK<br>- FK<br>- Not Null|      
| nome | Nome da habilidade | Char | 100 | - Not Null|      
| nivel | Nível da habilidade | INT |  | - Not Null|      
| coolDown | Tempo de recarga | INT |  | - Not Null|   
| danoMitigado | Indica o tanto de dano mitigado possibilitado pela defesa | INT          |         | - Not Null    
|preco| Custo da defesa|INT||- Not Null|

<!-- ludmila alterou -->
## Entidade: setor

**Descrição:** A entidade `Setor` descreve um setor que está dentro do campus. A chave primária composta indica que o mesmo id_setor poderia existir em mais de um campus, mas com distinção pelo id_campus. Possui informação de nome, descrição, identificador do campus, e duas chaves estrangeiras referenciando outras lomocomoções para acesso de outros setores, na qual, possui um auto-relacionamento em que a partir de um setor pode se chegar a outro, ou seja, esse relacionamento entre os setrores cria um tipo de estrutura de lista duplamente ligada. Essa estrutura pode ser útil para organizar setores em ordem (por exemplo, geográfica ou lógica). Os campos id_prevSetor e id_proxSetor são auto-relacionamentos com a mesma tabela, ideais para navegação sequencial entre setores.

| Nome         | Descrição                                  | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ------------ | ------------------------------------------ | ------------ | ------- | ------------------------------------------------------------------ |
| id_setor     | Identificador do Setor                     | INT      |         | - PK<br>- Not Null<br>- Identity                                                |
| id_campus    | Identificador do Campus                    | INT      |         | - PK<br>- FK<br>- Not Null                                        |
| nome         | Nome do Setor                              | Char      | 100     | - Not Null                                                         |
| descricao    | Descrição do Setor                         | Char      | 255     | - Not Null                                                         |
| id_proxSetor | Identificador do próximo setor(auto-relacion.) | INT      |        | - FK<br>- Not Null                                              |
| id_prevSetor | Identificador do setor anterior            | INT      |       | - FK<br>- Not Null                                                 |

<!-- ludmila alterou -->
## Entidade: loja_item

**Descrição**: A tabela `loja_item` representa a relação entre as lojas disponíveis no sistema e os itens que estão à venda em cada uma delas. Essa tabela é usada para modelar o relacionamento muitos-para-muitos entre Loja (presente em sala) e Item, indicando quais itens estão disponíveis em quais lojas.


| Nome | Descrição | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ---- | --------- | ------------ | ------- | ------------------------------------------------------------------ |
|id_sala|Identificador da sala|INT||- PK<br>- FK<br>- Not Null|
|id_item|Identificador de item|INT||- PK<br>- FK<br>- Not Null|

<!-- ludmila alterou -->
## Entidade: tipo_item

**Descrição**: A tabela `tipo_item` é uma tabela auxiliar resultado de uma generalização/especialização Total Exclusiva. Armazena o identificador do item (que é uma chave primária) e de seu tipo, que .


| Nome      | Descrição             | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| --------- | --------------------- | ------------ | ------- | ------------------------------------------------------------------ |
| id_item   | Identificador do item | INT     |       | - PK<br>- Not Null<br>- Identity                                                 |

| item_tipo | Indica o tipo do item | Char      | 10     | - Not Null<br>- Check ('Consumível', 'Equipável', 'Monetário', 'Relíquia')                                                         |

<!-- ludmila alterou -->
## Entidade: reliquia

**Descrição**: A tabela reliquia armazena os dados das relíquias disponíveis no sistema e possuem um tipo específico. Cada relíquia possui um identificador único, um nome, descrição e um tipo, que relaciona-se a um tema.

| Nome          | Descrição                   | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ------------- | --------------------------- | ------------ | ------- | ------------------------------------------------------------------ |
| id_reliquia   | Identificador da relíquia   | INT      |        | - PK<br>- FK<br>- Not Null                                                  |
| nome   | Nome da relíquia   | Char      |   100     | - Not Null                                                 |
| descricao   | Descrição da relíquia   | Char      |  255      | - Not Null                                                 |
| tipo_reliquia | Descreve o tema da relíquia | Char      | 100     | - Not Null                                                         |

<!-- ludmila alterou -->
## Entidade: consumivel

**Descrição:** A entidade `Consumível` descreve um item consumível. Cada item consumível possui um identificador único, um nome, descrição e possui informações como efeito e preço.

| Nome   | Descrição                             | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ------ | ------------------------------------- | ------------ | ------- | ------------------------------------------------------------------ |
| id_item | Identificador do item | INT          |         | - PK<br>- FK<br>- Not Null                                                         |
| nome   | Nome do item   | Char      |   100     | - Not Null                                                 |
| descricao   | Descrição do item   | Char      |  255      | - Not Null                                                 |
| efeito  | Efeito do item              | FLOAT        |         | - Not Null                                                         |
| preco  | Preço do item consumível              | FLOAT        |         | - Not Null                                                         |

<!-- ludmila alterou -->
## Entidade: equipavel

**Descrição:** A entidade `Equipavel` descreve um item equipável. Cada item equipável possui um identificador único, um nome, descrição e possui informações como efeito, preço e se está equipado ou não.

| Nome | Descrição | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ---- | --------- | ------------ | ------- | ------------------------------------------------------------------ |
| id_item | Identificador do item | INT          |         | - PK<br>- FK<br>- Not Null                                                         |
| nome   | Nome do item   | Char      |   100     | - Not Null                                                 |
| descricao   | Descrição do item   | Char      |  255      | - Not Null                                                 |
| efeito  | Efeito do item              | FLOAT        |         | - Not Null                                                         |
| preco  | Preço do item consumível              | FLOAT        |         | - Not Null                                                         |
| equipado |indica se o item equipavel está equipado ou não | BOOLEAN | 1 bit |- Not Null |

<!-- ludmila alterou -->
## Entidade: monetario

**Descrição:** A tabela `monetario` representa itens do tipo monetário no sistema, como moedas ou valores que podem ser acumulados pelos jogadores. Essa tabela especializa a tabela item e define o valor numérico associado a esse tipo de recurso. Herda todos os atributos de Item.

| Nome | Descrição | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ---- | --------- | ------------ | ------- | ------------------------------------------------------------------ |
| id_item | Identificador do item | INT |         | - PK<br>- FK<br>- Not Null                                                         |
| nome   | Nome do item   | Char      |   100     | - Not Null                                                 |
| descricao   | Descrição do item   | Char      |  255      | - Not Null                                                 |
| valor | O valor do item monetário | INT |    | - Not Null |


<!-- ludmila alterou -->
## Entidade: sala_comum

**Descrição:** A tabela `sala_comum` representa as salas que compõem um setor dentro da estrutura do sistema. Cada sala está vinculada a um setor (id_setor) e possui um identificador próprio (id_sala). A estrutura permite o encadeamento de salas por meio de relacionamentos de anterior e próxima (id_prevSala e id_proxSala), formando uma sequência navegável. Além disso, cada sala pode conter funcionalidades específicas como loja (tem_loja) e dungeon (tem_dungeon), representadas por campos booleanos. Essa modelagem permite a navegação sequencial entre salas e a definição de pontos especiais dentro de um setor.

| Nome | Descrição | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ---- | --------- | ------------ | ------- | ------------------------------------------------------------------ |
|id_sala|Identificador único da sala|INT|  |- PK<br>- Not Null<br>- Identity|
|id_setor|Identificador do setor em que a sala está|INT|  |- PK<br>- FK<br>- Not Null<br>|
|nome | nome da sala|Char|100|- Not Null|
|descrição|Descrição do que tem/contem na sala|Char|255|- Not Null|
|id_prevSala | Identificador da sala anterior | INT |   |- FK<br>|
|id_proxSala | Identificador da próxima sala | INT |   |- FK<br>|
|tem_loja|Se a sala possui loja|BOOLEAN| 1 bit |- Not Null<br>|
|tem_dungeon|Se a sala possui dungeon|BOOLEAN| 1 bit |- Not Null<br>|

<!-- ludmila alterou -->
## Entidade: habilidade_criatura

**Descrição:** Cada registro da tabela `habilidade_criatura` indica que uma determinada criatura possui uma determinada habilidade.

| Nome | Descrição | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ---- | --------- | ------------ | ------- | ------------------------------------------------------------------ |
|id_criatura|Identificador da criatura|INT||- PK<br>- FK<br>- Not Null<br>|
|id_habilidade|Identificador da habilidade|INT||- PK<br>- FK<br>- Not Null<br>|

<!-- isaque alterou -->
## Entidade: habilidade_estudante

**Descrição:** A tabela Habilidade_Estudante indica quais habilidades cada estudante possui, permitindo que cada estudante possa ter diversas habilidades cadastradas.

| Nome | Descrição | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ---- | --------- | ------------ | ------- | ------------------------------------------------------------------ |
|id_estudante|Identificador do estudante|INT||- PK<br>- FK<br>- Not Null<br>|
|id_habilidade|Identificador da habilidade|INT||- PK<br>- FK<br>- Not Null<br>|

<!-- isaque alterou -->
## Entidade: habilidade_Loja

**Descrição:** A tabela Habilidade_Loja representa o relacionamento entre lojas e habilidades disponíveis para venda. Ela define quais habilidades podem ser adquiridas nas lojas.

| Nome | Descrição | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ---- | --------- | ------------ | ------- | ------------------------------------------------------------------ |
|id_loja|Identificador da loja|INT||- PK<br>- FK<br>- Not Null<br>|
|id_habilidade|Identificador da habilidade|INT||- PK<br>- FK<br>- Not Null<br>|

<!-- isaque alterou -->
## Entidade: Instancia_de_item

**Descrição:** Armazena as instâncias de itens que existem no sistema, associando cada item a uma sala e/ou a um estudante. Cada instância possui um identificador próprio e referencia um tipo de item. Esta tabela permite controlar a posse e localização dos itens no ambiente.

| Nome | Descrição | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ---- | --------- | ------------ | ------- | ------------------------------------------------------------------ |
|id_instanciaItem|Identificador da instância do item|INT||- PK<br>- Identity<br>|
|id_item|Identificador do item que foi instânciado|INT||- PK<br>- FK<br>- Not Null<br>|
|id_sala|Identificador da sala|INT||- FK<br>|
|id_estudante|Identificador do estudante|INT||- FK<br>|
|equipado|Item equipado|INT|||


<!-- isaque alterou -->
## Entidade: estudante

**Descrição:** A tabela Estudante armazena os dados principais dos estudantes que participam do sistema. Cada estudante possui atributos como vida, estresse e total de dinheiro acumulado. Essa tabela também indica a qual sala o estudante pertence, por meio de uma chave estrangeira.

| Nome | Descrição | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ---- | --------- | ------------ | ------- | ------------------------------------------------------------------ |
|id_estudante|Identificador de estudante|INT||- PK<br>- Identity<br>|
|id_sala|Identificador da sala que o estudante está|INT||- FK<br>- Not Null<br>|
|nome|Nome do usuário|Char|100|- Not Null|
|vida|Total de vida que o estudante tem|INT||- Not Null|
|estresse|o Nível de stress que o usuário está|INT||- Not Null|
|total_dinheiro|Total de moedas que o estudante tem|INT||- Not Null|

<!-- isaque alterou -->
## Entidade: monstro_simples

**Descrição:** A tabela monstro_simples representa criaturas do tipo simples (não-chefes) que aparecem no jogo. Esses monstros, ao serem derrotados, concedem uma certa quantidade de experiência temática (XP) ao jogador e podem deixar moedas como recompensa.Cada monstro possui atributos como nível, vida máxima, tipo e uma descrição que pode ser usada para fins narrativos ou funcionais no jogo. A tabela é uma especialização da entidade `tipo_criatura`.

| Nome | Descrição | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ---- | --------- | ------------ | ------- | ------------------------------------------------------------------ |
|id_criatura|Identificador da criatura|INT||- PK<br>- FK<br>- Not Null<br>|
|nivel|Nivel da criatura|INT|100|- FK<br>- Not Null<br>|
|vida_max|Valor da vida da criatura|INT||- Not Null|
|nome|Nome da criatura|Char|100|- Not Null<br>|
|descricao|Descriçao da criatura|Char|200|-Not Nul|
|xp_tema|Quanidade de pontos que o tema oferece para determinada criatura|INT||- Not Null<br>|
|qtd_moedas|Quantidades de moedas que o monstro dropa|INT||- Not Null<br> - CHECK (qtd_moedas >= 0)|

<!-- isaque alterou -->
## Entidade: tipo_criatura 

**Descrição:** A tabela tipo_criatura é uma tabela auxiliar resultado de uma generalização/especialização total exclusiva que armazena o id da criatura e de qual tipo ela é, se é monstro ou se é boss.

| Nome | Descrição | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ---- | --------- | ------------ | ------- | ------------------------------------------------------------------ |
|id_criatura| Identificador da criatura|INT||- PK<br>- Identity<br>|
|tipo_criatura|Tipo da criatura|Char|10|- Not Null<br> CHECK(tipo_criatura IN ('Monstro', 'Boss'))|

<!-- isaque alterou -->
## Entidade: afinidade

**Descrição:** A tabela Afinidade armazena o relacionamento entre estudantes e temas, representando o nível de domínio que cada estudante possui sobre determinado tema. Cada registro representa uma afinidade única entre um estudante e um tema. Esta tabela possui chave primária composta e duas chaves estrangeiras, referenciando as tabelas Estudante e Tema.


| Nome | Descrição | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ---- | --------- | ------------ | ------- | ------------------------------------------------------------------ |
|id_estudante|Identificador do estudante|INT||- PK<br>- FK<br>- Not Null|
|id_tema|Identificador do tema |INT| |- PK<br>- FK<br>- Not Null|
|xp_atual|xp atual que a afinidade tem|INT||- Not Null|
|nivel_atual|Qual o nível atual da afinidade|INT||- Not Null|

<!-- isaque alterou -->
## Entidade: tipoHabilidade

**Descrição:** É uma tabela auxiliar resultado de uma generalização/especialização total exclusiva. Essa tabela armazena o Id da habilidade e o tipo dela, podendo ser de ataque, cura ou defesa. A tabela se relaciona com as tabelas de Ataque, Cura e Defesa indicando o id das habilidades e com as tabelas de habilidade_criatura, habilidade_estudante, habilidade_loja indicandos as habilidades da criatura ou estudante e quais habilidades vendem na loja. 

| Nome | Descrição | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ---- | --------- | ------------ | ------- | ------------------------------------------------------------------ |
|id_habilidade | Identificador Da habilidade|INT||- PK<br> |
|tipo_habilidade|Qual o tipo da habilidade|Char|10|- Not Null<br>- CHECK('ataque', 'cura', 'defesa') |

<!-- isaque alterou -->
## Entidade: tema

**Descrição:** Contém as temáticas: Matemática, Programação, Engenharias, Gerais e Humanidades.

| Nome | Descrição | Tipo de dado | Tamanho | Restrições de domínio (PK, FK, Not Null, Check, Default, Identity) |
| ---- | --------- | ------------ | ------- | ------------------------------------------------------------------ |
|id_tema | Identificador do Tema|INT| |- PK<br>- Identity<br> |
|nome | nome do tema |Char|100|- Not Null<br>- CHECK(nome IN ('Matemática', 'Programação', 'Engenharias', 'Gerais', 'Humanidades'))|



## Histórico de Versões
| Versão |  Data  | Descrição| Autor                 |
| :----: | :--------: | ---------------------------------- | -------------------------------------------------------------------------------- |
| `1.0` | 01/05/2025 | Criação do Dicionário de Dados      | [Ludmila Nunes](https://github.com/ludmilaaysha) & [Isaque Camargos](https://github.com/isaqzin)|
| `2.0` | 10/06/2025 | Atualização do Dicionário de Dados      | [Milena Marques](https://github.com/milenamso)|
| `3.0` | 04/07/2025 | Segunda atualização do Dicionário de Dados | [Ludmila Nunes](https://github.com/ludmilaaysha) & [Isaque Camargos](https://github.com/isaqzin)|
