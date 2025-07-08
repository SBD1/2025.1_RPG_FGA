# 2025.1_RPG_FGA
Desenvolvimento de Game para a disciplina de Banco de Dados 1

## Entregas

Para acessar nossas entregas, clique no link abaixo:

[https://sbd1.github.io/2025.1_RPG_FGA/](https://sbd1.github.io/2025.1_RPG_FGA/)

---

## Como Rodar a Aplicação

Siga estes passos para configurar o ambiente de desenvolvimento e o banco de dados.

### Pré-requisitos

Antes de começar, garanta que você tenha os seguintes softwares instalados em seu sistema (ambiente baseado em Debian/Ubuntu):

* **Python 3.8+**
* **PostgreSQL**
* **Git** (para clonar o repositório)

### 1. Clone o Repositório

Primeiro, clone o repositório do projeto para a sua máquina local:

```bash
git clone https://github.com/SBD1/2025.1_RPG_FGA.git
cd 2025.1_RPG_FGA
```

### 2. Configure o Banco de Dados
O projeto inclui um script de automação (```setup.sh```) que configura o banco de dados do zero. Ele irá:
* Apagar e recriar o banco de dados ```rpg_fga```.
* Criar o ```usuário``` estudante com a senha ```123```.
* Conceder as permissões de superusuário necessárias.
* Executar os scripts ```DDL.sql``` e ```DML.sql``` para criar e popular as tabelas.

Para executá-lo, navegue até a pasta ```docs/entrega3/scripts/``` e siga os comandos:
```bash
# Navegue até a pasta correta
cd docs/entrega3/scripts/

# Torne o script executável (só precisa fazer isso uma vez)
chmod +x setup.sh

# Execute o script de configuração
./setup.sh
```
> Nota: Você será solicitado a digitar a sua senha de usuário do sistema (a mesma usada para o comando ```sudo```). Isso é necessário para que o script possa executar comandos como o usuário ```postgres```.

### 3. Configure o Ambiente Virtual Python
É uma boa prática usar um ambiente virtual para isolar as dependências do projeto.
```bash
# Ainda na pasta 'scripts'

# Crie o ambiente virtual (criará uma pasta .venv)
python3 -m venv .venv

# Ative o ambiente virtual
source .venv/bin/activate
```
> Você saberá que o ambiente está ativo pois ```(.venv)``` aparecerá no início do seu prompt do terminal.

### 4. Instale as Dependências
Com o ambiente virtual ativo, instale a biblioteca necessária para a conexão com o PostgreSQL:
```
pip install psycopg2-binary
```
### 5. Execute a Aplicação
Com o ambiente configurado e o banco de dados populado, você já pode iniciar o jogo!
1. Garanta que seu ambiente virtual esteja ativo (```source .venv/bin/activate```).
2. Execute o arquivo principal da aplicação:
```bash
python3 app.py
```
O menu inicial do jogo deverá aparecer no seu terminal. Divirta-se!

## Integrantes

<font size="3"><p style="text-align: center">Tabela 1: Integrantes do grupo</p></font> 

<table align="center">
  <tr>
    <td align="center">
      <img src="https://github.com/isaqzin.png" width=100><br>
      <b><a href="https://github.com/isaqzin">Isaque Camargos</a></b><br>
    </td>
    <td align="center">
      <img src="https://github.com/ludmilaaysha.png" width=100><br>
      <b><a href="https://github.com/ludmilaaysha">Ludmila Nunes</a></b><br>
    </td>
    <td align="center">
      <img src="https://github.com/milenamso.png" width=100><br>
      <b><a href="https://github.com/milenamso">Milena Marques</a></b><br>
    </td>
    <td align="center">
      <img src="https://github.com/bolzanMGB.png" width=100><br>
      <b><a href="https://github.com/bolzanMGB">Othavio Bolzan</a></b><br>
    </td>
    <td align="center">
      <img src="https://github.com/rafaelschadt.png" width=100><br>
      <b><a href="https://github.com/rafaelschadt">Rafael Welz</a></b><br>
    </td>
    <td align="center">
      <img src="https://github.com/rodrigoFAmaral.png" width=100><br>
      <b><a href="https://github.com/rodrigoFAmaral">Rodrigo Amaral</a></b><br>
    </td>
  </tr>

</table>

<font size="2"><p style="text-align: center">Fonte: Autores, 2025</p></font> 