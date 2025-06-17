# 1\. Objetivo Principal:

Coletar todas relíquias acadêmicas para concluir o jogo. São ao total 5 relíquias, cada uma dropada de um chefão específico.

# 2\. Estrutura geral do campus (MAPA).

* Campus:  
  * Setores:   
    * UED;  
    * UAC;   
    * Graminha;   
    * Refeitório Universitário;  
    * Containers;  
    * Formatura (exclusivo final)

* Dentro dos Setores:  
  * Salas comuns:   
    * Loja;  
    * Dungeon Acadêmica


* Dungeon Acadêmica com:  
  * Boss temático:  
  * Monstros temáticos;


Setores espalhados pelo campus, ao total, 6 setores.

# 3\. Estudante.

O estudante é o personagem controlável do jogo, cada jogador terá seu estudante, que carregará os seguintes atributos.

* Nome;  
* ID;  
* Pontos de Vida;  
* Pontos de Estresse;  
* Catálogo de habilidades;  
* “Inventário”;  
* Afinidades com os temas.

O estudante poderá entrar em combate contra as criaturas, e utilizará de suas habilidades para derrotá-las. Além do combate, haverá área de exploração para a coleta e compra de itens que o ajudarão na jornada. A compra dos itens será feita através de moedas, do qual, poderá ser encontrada pelo mapa ou dropadas de monstros simples.

3.1. Sistema de Afinidade.

No RPG \- FGA, haverá um sistema de afinidade para cada estudante, relacionando ele com os 5 temas presentes no jogo. 

Esse sistema, permite rastrear a evolução do estudante em cada área, possibilitando-o de evoluir de forma parelha ou focar apenas um tema, se quiser, se adaptando a forma como cada jogador gosta de jogar.

Para cada estudante, haverá uma relação de afinidade (nível) com um tema dentro de jogo. Para evoluir sua afinidade em um determinado tema, é necessário conseguir XP daquele tema, tal qual, se consegue derrotando monstros simples dessa temática.

Subir de nível em cada tema é importante, pois permite a compra e o desbloqueio de novas habilidades, fortalecendo o estudante e aprimorando seu arsenal.

# 3.2. Itens.

Os itens presentes no RPG \- FGA, serão de enorme utilidade para ajudar o estudante a cumprir a sua jornada.  
Haverá, itens de 4 tipos diferentes.

- **Consumíveis** (Comidas e Itens para recuperar pontos de vida e estresse)  
- **Não consumíveis** (Itens para auxiliar no combate, aumentando vida máxima e etc)  
- **Relíquias** (Drops especiais de bosses, necessárias para zerar o jogo)  
- **Monetário** (Moedas para realizar comprar e trocas)

# 4\. Sistema de Habilidades.

As habilidades serão a ferramenta central do combate dentro do RPG \- FGA. Cada monstro e estudante contará com seu próprio catálogo de habilidades, que ao longo do jogo, poderá ser modificado e ampliado. Há 3 tipos de habilidades, Ataque \- A, Defesa \- D e Cura \- C. 

Cada habilidade, além de ser categorizada como “A”, “D” ou “C”, será também categorizada por um único tema, sendo estes; (Matemática \- M, Programação \- P, Engenharias \- E, Humanidades \- H, Gerais \- G).

As habilidades, em geral, possuem características em comum, como nome, descrição e cooldown.

# 4.1. Sistema de Combate.

O combate é uma das principais mecânicas do RPG \- FGA, e será realizado através do uso de habilidades e estratégia.  
O combate será feito de turnos, e poderá ter 3 resultados possíveis. 

- Vitória do jogador.  
- Vitória da criatura.  
- Fuga do jogador.

No caso da vitória, vence o jogador/criatura que tirar todos os pontos de vida do adversário.

A cada turno do combate, o monstro e o jogador vão escolher uma habilidade. Segue uma lista dos resultados de cada escolha:

**Tabela de possíveis resultados por turno** 

| Habilidade do Jogador | Habilidade do Monstro | Resultado |
| :---: | :---: | :---: |
| A | A | Ambos perdem pontos de vida de acordo com a potência de cada ataque. |
| A | D | Desconta-se do ataque os pontos de defesa, se por um acaso, o resultado desse decréscimo for menor ou igual a zero, o ataque é anulado completamente. |
| D | A | Mesma situação anterior |
| D | D | Nada ocorre |
| C | C | Ambos se curam |
| A | C | A cura é interrompida e o monstro sofre o dano total do ataque. |
| C | A | A cura é interrompida e o jogador sofre o dano total do ataque. |
| D | C | O monstro se cura |
| C | D | O jogador se cura |

Sempre a cada turno, o jogador pode escolher fugir do combate, caso veja que o monstro é um nível muito avançado para combater.

Todo duelo/combate no jogo custa estresse do jogador, mesmo que perca, ganhe ou fuja.

Consumo de estresse por situação:

- Em caso de vitória (baixo)  
- Em caso de fuga (médio)  
- Em caso de derrota (alto)

Caso fuja, o jogador terá parte do seu estresse consumido, dependendo do nível de diferença entre o monstro e o jogador. Quanto maior seja essa diferença, menor é o estresse consumido.

Em caso de vitória do jogador, o mesmo será recompensado com moedas e xp para o tema relacionado com aquela criatura. (Se a criatura for um boss, será dropada uma relíquia ao invés de moedas e xp). 

Por último, em caso de derrota, além de ter muito estresse consumido, perderá parte das moedas que carrega com si.

# 4.2. Sistema de Eficácia.

O sistema de eficácia do RPG \- FGA é responsável por adicionar mais dinâmica no jogo, “buffando” e “nerfando” habilidades a depender da sua temática.

Resumindo, cada habilidade há um tema associado, e cada tema é eficiente, neutro e não-eficiente contra outros temas. Segue o exemplo.

Temas presentes dentro do RPG-FGA:

- Matemática (M)  
- Programação (P)  
- Humanidades (H)  
- Engenharias (E)  
- Gerais (G)


**Tabela dos temas e suas respectivas eficiências**

| Tema | Forte Contra | Neutro | Fraco Contra |
| :---: | :---: | :---: | :---: |
| Matemática | P | M, E, G | H |
| Programação | E | P, H, G | M |
| Humanidades | M | E, P, H | G |
| Engenharias | G | M, H, E | P |
| Gerais | H | M, P, G | E |

A partir dessa tabela, conseguimos complementar nosso sistema de combate. Além da tabela de resultados dos turnos, agora teremos uma segunda variável, a “eficácia dos temas”. 

Para cada resultado de turno, será também analisado os temas das habilidades, aplicando um multiplicador no resultado final da habilidade conjurada. 

Logo, há dois possíveis casos de combinação de temas.

1. Temas “opostos”, as habilidades jogadas no turno contém temas opostos, ou seja, fraco ou forte contra.  
2. Temas “neutros”, as habilidades jogadas no turno contém temas neutros, ou seja, temas neutros entre si.

Para o primeiro caso, a habilidade que tiver o tema forte, será beneficiada de um multiplicador de 1,5x, seja ela de ataque, defesa ou cura. E a habilidade com o tema fraco, terá uma multiplicador de 0,75x em seus atributos.

Segue um exemplo.

- Suponha que em um turno aleatório, um jogador profira uma habilidade de defesa (20pts), do qual o seu tema é de programação. E também, nesse mesmo turno, um monstro profira um ataque de engenharias (40pts)


- Pela lógica anterior, sem considerar os temas, o ataque tem maior potência que a defesa (40 \> 20). Logo, o dano que o jogador sofreria, seria de 20 pts no total, visto que, 40 \- 20 \= 20  
- Porém, como nesse caso, programação e engenharias são temas “opostos”, nesse caso Programação é forte contra Engenharias, o multiplicador entrará em vigor, alterando o resultado do turno da seguinte maneira.

- Defesa (20 pts) \[TEMA FORTE\]   X     Ataque (40 pts) \[TEMA FRACO\]  
- Defesa (20 pts) (1,5x)                     X     Ataque (40 pts) (0,5x)  
- Defesa (30 pts)                                X     Ataque (30 pts)  
    
- Resultado final, 30 \- 30 \= 0, logo, o ataque foi absorvido completamente.

- (Ressaltando que até para casos de A x C, onde os ataques cancelam a cura, o multiplicador ainda valerá caso sejam de temas opostos. Ou seja, mesmo que a cura seja cancelada, e seu tema seja forte contra o ataque realizado, o ataque ainda sofrerá de um multiplicador de 0,75x)


Para o segundo caso, não haverá multiplicador, e apenas a potência de cada habilidade será levada em consideração.

# 5\. Criaturas.

As criaturas do RPG \- FGA podem ser divididas em duas categorias:

- Bosses  
- Monstros Simples

Tanto bosses e monstros simples, contém características comuns, como nome, vida, a dungeon da qual pertence, o seu conjunto de habilidades e etc.

A diferença se dá no drop deixado e na força de cada um. Monstros simples são mais fracos, possuem habilidades mais iniciais e dropam apenas xp e moeda.

Já os bosses, além de mais vida e habilidades mais fortes, contam com um drop especial denominado relíquia. Além de que, cada boss pode ser derrotado apenas uma única vez. Já os monstros simples, podem ser utilizados para farm.

# 5.1 Salas Comuns, Lojas e Dungeons Acadêmicas.

As salas comuns estarão muito presentes no cenário do RPG \- FGA, e fornecerá o background de exploração e compra necessário para o estudante se fortalecer. 

Cada sala comum, é conectada a outras salas comuns, e também, é passível de conter uma loja e/ou uma dungeon acadêmica dentro delas.

As lojas, por sua vez, são responsáveis por vender itens e habilidades. Tudo que é vendido na loja custa moedas, contudo, além de moedas, as habilidades necessitam um nível mínimo do jogador naquela determinada afinidade. 

(OBS: Nem todos os itens e nem todas as habilidades estarão presentes numa loja só, fazendo que, o player tenha que visitar outras lojas pelo mapa para achar o que procura)

Outro ponto relevante a se firmar, nem todos os itens são passíveis de compra, apenas os itens consumíveis para efeito imediato. Itens não consumíveis e relíquias são encontrados de outras maneiras.

Finalizando, a dungeon acadêmica é a área de contato do jogador com as criaturas. Toda dungeon acadêmica é regida por um tema, e esse tema guiará o nascimento das criaturas naquela dungeon. Para cada dungeon acadêmica, existem infinitos monstros simples e apenas um boss.

Uma vez que o boss é derrotado, a dungeon acadêmica se fecha, e a relíquia é dropada ao jogador, finalizando uma temática.

## Histórico de Versões
| Versão |  Data  | Descrição| Autor                 |
| :----: | :--------: | ---------------------------------- | -------------------------------------------------------------------------------- |
| `1.0` | 16/06/2025 | Criação da história e mecânicas  | [Rafael Welz](https://github.com/rafaelschadt)|

