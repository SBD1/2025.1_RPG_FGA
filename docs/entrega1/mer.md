# **MER \- Modelo Entidade-Relacionamento do Sistema RPG**

O Modelo Entidade-Relacionamento de um banco de dados é um modelo conceitual que descreve as entidades de um domínio de negócios, com seus atributos e seus relacionamentos.

---

### **1\. Entidades**

1. Campus  
2. Dungeon Academica   
3. Boss   
4. Gabinete Boss   
5. Ataque   
6. Cura   
7. Defesa   
8. Setor   
9. Loja   
10. Item   
11. Reliquia   
12. Consumivel   
13. Equipavel   
14. Sala Comum   
15. Inventario   
16. Instancia de item   
17. Batalha   
18. Duelo   
19. Estudante   
20. Monstro   
21. Afinidade   
22. Habilidades   
23. Instancia de monstro 

---

### **2\. Atributos**

* **Campus:** nome, descricao, id\_campus;   
* **Dungeon Academica:** id\_dungeon, id\_sala, nome, descricao, afinidade\_tipo;   
* **Boss:** id\_boss, id\_gabinete\_boss, nome, vida, id\_Habilidades, tipo\_afinidade;   
* **Gabinete Boss:** id\_gabinete\_boss, id\_dungeon;   
* **Ataque:** danoCausado, porcentagemAcerto;   
* **Cura:** vidaRecuperada;   
* **Defesa:** danoMitigado;   
* **Setor:** id\_setor, nome, id\_campus, descricao, id\_proxSetor, id\_prevSetor;   
* **Loja:** id\_loja, nome, id\_instanciaitem, id\_Habilidade, id\_sala;   
* **Item:** descricao, nome, id\_item, item\_tipo;   
* **Reliquia:** id\_reliquia, tipo\_reliquia;   
* **Consumivel:** efeito, preco;   
* **Equipavel:** efeito, preco, equipado;   
* **Sala Comum:** id\_sala, id\_instanciaitem, nome, descricao, id\_setor;   
* **Inventario:** id\_inventario, id\_instanciaitem;   
* **Instancia\_de\_item:** id\_item, id\_instanciaitem;   
* **Batalha:** player\_win, moedas, xp\_area, estresse\_gasto, id\_batalha, id\_instanciaMonstro;   
* **Duelo:** player\_win, moedas, estresse\_gasto, id\_duelo, id\_instanciaitem, id\_boss;   
* **Estudante:** id\_estudante, nome, vida, estresse, total\_moedas, id\_inventario, id\_Habilidades, id\_afinidade, id\_sala;   
* **Monstro:** id\_Monstro, id\_Habilidade, vidaMax, Nome, tipo\_setor;   
* **Afinidade:** xp\_max, nivel\_atual, xp\_atual, id\_afinidade, tipo\_afinidade;   
* **Habilidades:** id\_Habilidade, nome, tipoHabilidade, nivel, afinidadeTipo, tipoHabilidade, cooldown, desbloqueado;   
* **Instancia de monstro**: id\_Monstro, vidaAtual, id\_instanciamonstro, id\_Dungeon; 


---

### **3\. Relacionamentos**

1. **Campus *contém* Setor**   
    * O Campus poderá possuir no mínimo um setor e no máximo vários setores (1,N).  
    * Um Setor só pode estar em exatamente um Campus (1,1).  
2. **Setor *conecta* Setor**   
    * Um setor pode conectar exatamente a um setor anterior(1,1)  
    * Um setor pode conectar a exatamente a um setor próximo(1,1)  
3. **Sala *contém* Dungeon Acadêmica**   
    * Uma sala pode possuir zero ou uma dungeon académica (0,1).  
    * Uma Dungeon Acadêmica só pode estar contida em exatamente um sala (1,1).  
4. **Setor *contém* Sala Comum**   
    * Um Setor pode conter nenhum a várias Salas Comuns (0,N).  
    * Uma Sala Comum só pode estar contida em exatamente um Setor (1,1).  
5. **Loja *contém* id da Sala**  
    * Uma sala pode conter nenhuma ou várias Loja (0,N).  
    * Uma loja só pode estar contida em exatamente uma sala (1,1).  
6. **Loja *vende* Habilidades**  
    * Uma Loja pode vender uma ou várias Habilidades (1,N).  
    * Uma Habilidade pode ser vendida por nenhuma ou várias Loja (0,N).  
7. **Loja *vende* Instância de Item**  
    * Uma Loja pode vender uma ou várias Instância de Item (1,N).  
    * Uma Instância de Item pode ser vendida por nenhuma ou várias Loja (0,N).  
8. **Salas Comuns *contém* Instância de Item**  
    * Uma Sala Comum pode conter nenhuma ou várias Instância de Item (0,N).  
    * Uma Instância de Item pode estar contida por nenhuma ou várias Salas Comuns (0,N).  
9. **Dungeon Acadêmica *contém* Instância de Monstro**   
    * Uma Dungeon Acadêmica pode conter um ou vários Monstros (1,N).  
    * Uma instância de monstro pode estar contido em apenas uma Dungeon Acadêmica (1,1).  
10.  **Dungeon Acadêmica *contém* Gabinete do Boss**   
    * Uma Dungeon Acadêmica pode conter apenas um Gabinete do Boss (1,1).  
    * Um Gabinete do Boss pode estar contido em apenas uma Dungeon Acadêmica (1,1).  
11.  **Instância de Monstro *gera* Monstro**   
    * Uma instância de monstro pode gerar exatamente um monstro (1,1).  
    * Um monstro pode ser gerado por nenhuma ou várias instâncias de monstro (0,N).  
12.  **Gabinete do Boss *contém* Boss**   
    * Um Gabinete do Boss pode conter apenas um Boss (1,1).  
    * Um Boss pode estar contido em apenas um Gabinete do Boss (1,1).
13.  **Boss *contém* Habilidades**   
    * Um boss possui no mínimo um e no máximo várias habilidades. (1,N).
    * Uma Habilidade pode ser possuída por no mínimo nenhuma e no máximo várias Boss (0,N).
14.  **Monstro *contém* habilidades**   
    * Um Monstro possui no mínimo um e no máximo várias Habilidades. (1,N).
    * Uma Habilidade pode ser possuída por no mínimo 0 e no máximo N Monstros (0,N).
15.  **Estudante *contém* habilidades**   
    * Um estudante possui no mínimo um e no máximo várias Habilidades. (1,N).
    * Uma Habilidade pode ser possuída por no mínimo nenhuma e no máximo vários estudantes (0,N).
16.  **Estudante *contém* Inventário**   
    * Um estudante pode possuir no mínimo um inventário, e no máximo um (1,1).
    * Um inventário pode conter no mínimo apenas um estudante e no máximo um (1,1).
17.  **Inventário *armazena* Instância de Item**   
    * Um inventário pode ter no mínimo nenhuma instância de item e no máximo varias (0,N).
    * Uma instância de item pode conter no mínimo nenhum inventário e no máximo um inventário (0,1).
18. **Instância de item *é gerada* por item**   
    * Uma instância de item pode gerar no mínimo um item, e no máximo apenas um item (1,1).
    * Um item pode ser gerado por nenhuma instância de item e no máximo varias (0,N).
19. **Relíquia *dropada em um* Duelo**   
    * Uma relíquia pode dropar no mínimo nenhum encontro de duelo e no máximo vários duelos (0,N).
    * Um duelo pode dropar no mínimo nenhuma relíquia, e no máximo varias relíquias (0,N).
20.  **Estudante *batalha com* monstro**   
    * Um estudante pode batalhar com no mínimo zero e no máximo um monstro (0,1).  
    * Um monstro pode batalhar com no mínimo zero e no máximo um estudante(0,1).  
21. **Estudante *duela com* Boss**   
    * Um estudante pode batalhar com no mínimo zero e no máximo um boss (0,1).  
    * Um boss pode batalhar com no mínimo zero e no máximo um boss (0,1).
22. **Estudante *contém* afinidade**   
    * Um estudante pode conter no mínimo uma afinidade e no máximo várias afinidades (1,N).  
    * Uma afinidade pode conter no mínimo nenhum estudante e no máximo vários estudante (0,N).
23. **Estudante *está em* sala**   
    * Um estudante pode estar inserido em uma sala ou no máximo uma sala (1,1).
    * Uma sala pode conter nenhum estudante ou no máximo vários estudantes (0,N).

| Versão |  Data  | Descrição| Autor                 |
| :----: | :--------: | ---------------------------------- | -------------------------------------------------------------------------------- |
| `1.0` | 01/05/2025 | Criação do documento MER      | [Rodrigo Amaral](https://github.com/rodrigoFAmaral) & [Milena Marques](https://github.com/milenamso)|
| `1.1` | 02/05/2025 | Fazendo correções no MER      | [Milena Marques](https://github.com/milenamso)|