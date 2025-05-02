# **MER \- Modelo Entidade-Relacionamento do Sistema RPG**

O Modelo Entidade-Relacionamento de um banco de dados é um modelo conceitual que descreve as entidades de um domínio de negócios, com seus atributos e seus relacionamentos.

---

### **1\. Entidades**

1. Campus  
2. Dungeon\_Academico  
3. Boss  
4. Gabinete\_Boss  
5. Ataque: danoCausado  
6. Cura  
7. Defesa  
8. Setor  
9. Loja  
10. Itens  
11. Reliquia  
12. Consumiveis  
13. Equipaveis  
14. Salas Comuns  
15. Inventario  
16. Instancia\_de\_item  
17. Batalha  
18. Duelo  
19. Estudante  
20. Monstro  
21. Afinidade  
22. NivelMatematica  
23. NivelProgramacao  
24. NivelHumanidade  
25. NivelEngenharia  
26. Habilidades

---

### **2\. Atributos**

* **Campus:** nome, descricao, id\_Campus;  
* **Dungeon\_Academico:** id\_dungeon, nome, descricao, afinidade\_tipo;  
* **Boss:** id\_boss, id\_dungeon, nome, id\_catalogo\_boss;  
* **Gabinete\_Boss:** id\_gabinete, id\_dungeon;  
* **Ataque:** danoCausado, porcentagemAcerto;  
* **Cura:** vidaRecuperada;  
* **Defesa:** danoMitigado;  
* **Setor:** id\_setor, nome, descricao, prox\_setor;  
* **Loja:** id\_loja, nome, itens, habilidades;  
* **Itens:** descricao, nome, id\_item;  
* **Reliquia:** origem;  
* **Consumiveis:** efeito, preco;  
* **Equipaveis:** reliquia, consumiveis, equipaveis;  
* **Salas Comuns:** id\_Sala, nome, descricao;  
* **Inventario:** id\_inventario;  
* **Instancia\_de\_item:** id\_inventario;  
* **Batalha:** player\_win, moedas, xp\_area, estresse\_gasto, drop, id\_batalha;  
* **Duelo:** player\_win, moedas, reliquia, estresse\_gasto, id\_duelo;  
* **Estudante:** id\_estudante, nome, vida, estresse, total\_moedas, inventario, catalogo\_de\_habilidades;  
* **Monstro:** id\_monstro, in\_Dungeon, habilidade, vida, Nome;  
* **Afinidade:** xp\_min, xp\_max, nivel\_atual, xp\_atual, id\_afinidade;  
* **NivelMatematica**  
* **NivelProgramacao**  
* **NivelHumanidade**  
* **NivelEngenharia**  
* **Habilidades:** id\_habilidades, nome, tipo\_habilidade, nivel, total\_moedas, inventario, catalogo\_de\_habilidades;


---

### **3\. Relacionamentos**

1. **Campus *contém* Setor**  
    - O Campus possui exatamente seis setores (6,6).  
    - Um Setor só pode estar em exatamente um Campus (1,1).  
2. **Setor *contém* Dungeon Acadêmica**  
    - Um Setor possui exatamente uma Dungeon Acadêmica (1,1).  
    - Uma Dungeon Acadêmica só pode estar contida em exatamente um Setor (1,1).  
3. **Setor *contém* Salas Comuns**  
    - Um Setor pode conter nenhum a várias Salas Comuns (0,N).  
    - Uma Sala Comum só pode estar contida em exatamente um Setor (1,1).  
4. **Setor *contém* Loja**  
    - Um Setor pode conter nenhuma ou várias Loja (0,N).  
    - Uma Loja só pode estar contida em exatamente um Setor (1,1).  
5. **Loja *vende* Habilidades**  
    - Uma Loja pode vender uma ou várias Habilidades (1,N).  
    - Uma Habilidade pode ser vendida por nenhuma ou várias Loja (0,N).  
6. **Loja é *visitada por* Estudante**  
    - Uma Loja pode ser visitada por apenas um Estudante (1,1).   
    - Um Estudante pode visitar nenhuma ou várias Loja  (0,N). \*\*(1,N)\*\*  
7. **Loja *vende* Instância de Item**  
    - Uma Loja pode vender uma ou várias Instância de Item (1,N).  
    - Uma Instância de Item pode ser vendida por nenhuma ou várias Loja (0,N).  
8. **Salas Comuns *contém* Instância de Item**  
    - Uma Sala Comum pode conter nenhuma ou várias Instância de Item (0,N).  
    - Uma Instância de Item pode estar contida por nenhuma ou várias Salas Comuns (0,N).  
9. **Dungeon Acadêmica *contém* Monstro \*\***  
    - Uma Dungeon Acadêmica pode conter um ou vários Monstros (0,N).  
    - Um Monstro pode estar contido em apenas uma Dungeon Acadêmica (1,1).  
10.  **Dungeon Acadêmica *contém* Gabinete do Boss**  
    - Uma Dungeon Acadêmica pode conter apenas um Gabinete do Boss (1,1).  
    - Um Gabinete do Boss pode estar contido em apenas uma Dungeon Acadêmica (1,1).  
11.  **Gabinete do Boss *contém* Boss**  
    - Um Gabinete do Boss pode conter apenas um Boss (1,1).  
    - Um Boss pode estar contido em apenas um Gabinete do Boss (1,1).  
12.  **Boss *contém* Catálogo de habilidades Boss**  
13.  **Monstro *contém* Catálogo de habilidades Monstro**  
14.  **Estudante *contém* Catálogo de habilidades Estudante**  
15.  **Estudante *contém* Inventário**  
    - Um estudante pode possuir no mínimo um inventário, e no máximo um (1,1)  
    - Um inventário pode conter no mínimo apenas um estudante e no máximo um (1,1)  
16.  **Inventário *contém* Instância de Item**  
    - Um inventário pode ter no mínimo nenhuma instância de item e no máximo varias (0,N)  
    - Uma instância de item pode conter no mínimo nenhum inventário e no máximo um inventário (0,1)  
17. **Instância de item *é gerada* por item**  
    - Uma instância de item pode gerar no mínimo um item, e no máximo apenas um item (1,1)  
    - Um item pode ser gerado por nenhuma instância de item e no máximo varias (0,N)  
18. **Instancia de item *dropada em um* Duelo**  
    - Uma instância de item pode dropar no mínimo em nenhum encontro de duelo e no máximo em vários duelos (0,N)  
    - Um duelo pode dropar no mínimo nenhuma instancia de item, e no máximo várias (0,N)  
19. **Instancia de item *é dropada em um* Encontro de Batalha**  
    - Uma instancia de item pode dropar no mínimo nenhuma batalha e no máximo várias batalhas (0,N)  
    - Uma batalha pode dropar no mínimo nenhuma instancia de item, e no máximo várias (0,N)  
20.  **Estudante *batalha com* monstro**  
    - Um estudante pode batalhar com no mínimo zero e no máximo um monstro (0,1).  
    - Um monstro pode batalhar com no mínimo zero e no máximo um estudante(0,1).  
21. **Estudante *duela com* Boss**  
    - Um estudante pode batalhar com no mínimo zero e no máximo um boss (0,1)  
    - Um boss pode batalhar com no mínimo zero e no máximo um boss (0,1)  
22. **Estudante *contém* afinidade**  
    - Um estudante pode conter no mínimo quatro afinidades e no máximo quatro (4,4)  
    - Uma afinidade pode conter no mínimo um estudante e no máximo um estudante (1,1)


| Versão |  Data  | Descrição| Autor                 |
| :----: | :--------: | ---------------------------------- | -------------------------------------------------------------------------------- |
| `1.0` | 01/05/2025 | Criação do documento MER      | [Rodrigo Amaral](https://github.com/rodrigoFAmaral) & [Milena Marques](https://github.com/milenamso)|