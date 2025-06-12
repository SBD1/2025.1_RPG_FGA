# **MER \- Modelo Entidade-Relacionamento do Sistema RPG**

O Modelo Entidade-Relacionamento de um banco de dados é um modelo conceitual que descreve as entidades de um domínio de negócios, com seus atributos e seus relacionamentos.

---

### **1\. Entidades**

1. Campus  
2. Dungeon Academica   
3. Boss   
4. Sala Comum
5. Ataque   
6. Cura   
7. Defea   
8. Setor   
9. Itens Loja   
10. Item   
11. Reliquia   
12. Consumivel   
13. Equipavel
14. Monetario
15. Criatura   
16. monstroSimples   
17. Instancia de item   
18. Habilidade Estudante   
19. Habilidade Criatura   
20. Estudante   
21. Habilidade Loja   
22. Afinidade   
23. Habilidades 
24. Tema
25. Instancia de criatura

---

### **2\. Atributos**

* **tema:** id\_tema, nome;   
* **habilidades:** id\_habilidade, id\_tema, nome, tipo\_habilidade, nivel, coolDown;   
* **criatura:** id\_criatura, vida\_max, tipo\_criatura, nome, nivel, descricao;   
* **campus:** id\_campus, nome, descricao;   
* **setor:** id\_setor, id\_campus, nome, descricao, id\_proxSetor, id\_prevSetor;   
* **sala_comum:** id\_sala, id\_setor, id\_prevSala, id\_proxSala, descricao, nome, tem\_loja, tem\_dungeon;   
* **estudante:** id\_estudante, id\_sala, nome, vida, estresse, total\_dinheiro;   
* **afinidade:** id\_estudante, id\_tema, xp\_atual, nivel\_atual;
* **dungeon_academica:** id\_dungeon, nome, descricao, id\_tema;   
* **boss:** id\_boss, id\_reliquia;   
* **reliquia:** id\_reliquia, tipo;   
* **monstro_simples:** id\_criatura, xp\_tema, qtd\_moedas;   
* **instancia\_de\_criatura:** id\_instanciaMonstro, id\_criatura, vida\_atual, id\_dungeon;   
* **item:** id\_item, nome, descricao, item\_tipo;   
* **consumivel:** id\_item, efeito, preco;   
* **instancia\_de\_item:** id\_item, id\_instanciaItem, id\_sala, id\_estudante;   
* **equipavel:** id\_item, efeito, preco, equipado;   
* **monetario:** id\_item, efeito, preco, equipado;   
* **loja\_item:** id\_sala, id\_item;   
* **habilidade\_criatura:** id\_criatura, id\_habilidade;   
* **habilidade\_estudante:** id\_estudante, id\_habilidade;   
* **loja:** id\_loja, nome;   
* **habilidade\_loja**: id\_loja, id\_habilidade;
* **ataque**: id\_habilidade, danoCausado, porcentagemAcerto;
* **cura**: id\_habilidade, danoCausado, porcentagemAcerto;
* **defesa**: id\_habilidade, danoMitigado; 



---

### **3\. Relacionamentos**

1. **Campus *contém* Setor**   ok
    * O Campus poderá possuir no mínimo um setor e no máximo vários setores (1,N).  
    * Um Setor só pode estar em exatamente um Campus (1,1).  
2. **Setor *conecta* Setor**   ok
    * Um setor pode conectar exatamente a um setor anterior(1,1)  
    * Um setor pode conectar a exatamente a um setor próximo(1,1)
3. **Sala_Comum *contém* Dungeon Acadêmica**   ok
    * Uma sala pode possuir zero ou uma dungeon académica (0,1).  
    * Uma Dungeon Acadêmica só pode estar contida em exatamente um sala (1,1).  
4. **Setor *contém* Sala Comum**   ok
    * Um Setor pode conter nenhuma a várias Salas Comuns (0,N).  
    * Uma Sala Comum só pode estar contida em exatamente um Setor (1,1).  
5. **Sala Comum *contém* Loja**  ok
    * Uma sala pode conter nenhuma ou várias Loja (0,N).  
    * Uma loja só pode estar contida em exatamente uma sala (1,1).  
6. **Loja *vende* Habilidades**  ok
    * Uma Loja pode vender uma ou várias Habilidades (1,N).  
    * Uma Habilidade pode ser vendida por nenhuma ou várias Loja (0,N).  
7. **Loja *vende* Item**  ok
    * Uma Loja pode vender nenhum ou vários itens (0,N).  
    * Uma Item pode ser vendida por nenhuma ou várias Loja (0,N).  
8. **Salas Comuns *contém* Instância de Item**  ok
    * Uma Sala Comum pode conter nenhuma ou várias Instância de Item (0,N).  
    * Uma Instância de Item pode estar contida por nenhuma ou várias Salas Comuns (0,N).  
9. **Dungeon Acadêmica *contém* Tema**   ok
    * Uma Dungeon Acadêmica pode conter apenas um tema (1,1).  
    * Um tema pode não estar contido em uma Dungeon e caso tiver, só pode ter um por Dungeon (0,1).  
10.  **Dungeon Acadêmica *contém* Instancia de Criatura** ok   
    * Uma Dungeon Acadêmica pode abrigar nenhuma instancia de criatura ou várias (0,N).  
    * Uma Instancia de Criatura pode estar contida em nenhuma Dungeon Acadêmica , e, no mínimo pode ser abrigada uma (0,1).  
11.  **Instancia de Criatura *gera* Monstro**   ok
    * Uma instância de criatura pode gerar exatamente um monstro (1,1).  
    * Um monstro pode ser gerado por nenhuma ou várias instâncias de criaturas (0,N).  
12.  **Criatura *domina* Habilidade** ok
    * Uma Criatura pode dominar uma ou várias habilidades(1,N).  
    * Uma Habilidade pode ser dominada cpor nenhuma ou várias criaturas(0,N).
13.  **Boss *contém* Habilidades**   
    * Um boss possui no mínimo um e no máximo várias habilidades. (1,N).
    * Uma Habilidade pode ser possuída por no mínimo nenhuma e no máximo várias Boss (0,N).
14.  **Monstro *contém* habilidades**   
    * Um Monstro possui no mínimo um e no máximo várias Habilidades. (1,N).
    * Uma Habilidade pode ser possuída por no mínimo 0 e no máximo N Monstros (0,N).
15.  **Estudante *domina* habilidades**   ok
    * Um estudante possui no mínimo um e no máximo várias Habilidades. (1,N).
    * Uma Habilidade pode ser possuída por no mínimo nenhum e no máximo vários estudantes (0,N).
16.  **Estudante *contém* Instancia de item**   ok
    * Um estudante pode possuir no mínimo nenhuma instancia de item, e no máximo várias (0,N).
    * Uma instancia de item pode conter no mínimo nenhum estudante e no máximo um (0,1).
17.  **Inventário *armazena* Instância de Item**   
    * Um inventário pode ter no mínimo nenhuma instância de item e no máximo varias (0,N).
    * Uma instância de item pode conter no mínimo nenhum inventário e no máximo um inventário (0,1).
18. **Instância de item *é gerada* por item** ok  
    * Uma instância de item pode gerar no mínimo um item, e no máximo apenas um item (1,1).
    * Um item pode ser gerado por nenhuma instância de item e no máximo varias (0,N).
19. **Relíquia *dropada em por* Boss**   ok
    * Uma relíquia pode ser dropada por no mínimo um boss e no máximo vários boss (1,N).
    * Um boss pode dropar uma relíquia (1,1).
20.  **Monetario *dropa* monstro simples**   ok
    * Um monetario pode dropar nenhuma monstro simples e no máximo vários(0,N).  
    * Um monstro simples pode ser dropado por nenhum monetario e no máximo vários(0,N).  
21. **Estudante *ataca* Instancia de Ciatura** ok
    * Um estudante pode batalhar com no mínimo zero e no máximo várias instancias de criaturas (0,N).  
    * Uma instancia de criatura pode atacar com no mínimo zero e no máximo um estudante (0,1).
22. **Estudante *aprende* afinidade**   ok
    * Um estudante pode aprender no mínimo cinco afinidades e no máximo cinco afinidades (5,5). 
    * Uma afinidade pode ser aprendida no mínimo por nenhum estudante e no máximo por vários estudantes (0,N).
23. **Estudante *está em* sala comum**   ok
    * Um estudante pode estar inserido em uma sala ou no máximo uma sala (1,1).
    * Uma sala pode conter nenhum estudante ou no máximo vários estudantes (0,N).
24. **Sala Comum *conecta* Sala Comum**   ok
    * Uma sala comum pode conectar exatamente uma sala anterior a ela(1,1)  
    * Uma sala comum pode conectar exatamente uma sala próxima a ela(1,1) 

| Versão |  Data  | Descrição| Autor                 |
| :----: | :--------: | ---------------------------------- | -------------------------------------------------------------------------------- |
| `1.0` | 01/05/2025 | Criação do documento MER      | [Rodrigo Amaral](https://github.com/rodrigoFAmaral) & [Milena Marques](https://github.com/milenamso)|
| `2.0` | 02/05/2025 | Fazendo correções no MER      | [Milena Marques](https://github.com/milenamso)|
|`3.0`| 12/06/2025 | Atualização do MER | [Milena Marques](https://github.com/milenamso)|
