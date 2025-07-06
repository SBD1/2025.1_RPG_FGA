import sys
from jogo.player.menu import menu_jogador
from jogo.db import get_db_connection
from jogo.db import clear_screen

def listar_estudantes_disponiveis():
    conn = get_db_connection()
    if not conn:
        print("Não foi possível conectar ao banco.")
        return []
    try:
        cur = conn.cursor()
        cur.execute("SELECT id_estudante, nome FROM estudante ORDER BY id_estudante")
        estudantes = cur.fetchall()
        # Faz strip nos nomes
        estudantes = [(id_, nome.strip()) for id_, nome in estudantes]
        return estudantes
    except Exception as e:
        print("Erro ao buscar estudantes:", e)
        return []
    finally:
        cur.close()
        conn.close()

def carregar_dados_estudante(id_estudante):
    conn = get_db_connection()
    if not conn:
        print("Não foi possível conectar ao banco.")
        return None
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT e.nome, e.vida, e.estresse, e.total_dinheiro, s.nome AS nome_sala, e.id_sala
            FROM estudante e
            JOIN sala_comum s ON e.id_sala = s.id_sala
            WHERE e.id_estudante = %s
        """, (id_estudante,))
        resultado = cur.fetchone()
        if not resultado:
            print("Estudante não encontrado.")
            return None
        
        nome, vida, estresse, total_dinheiro, nome_sala, id_sala = resultado
        return {
            "id": id_estudante,
            "nome": nome.strip(),
            "vida": vida,
            "estresse": estresse,
            "total_dinheiro": total_dinheiro,
            "nome_sala": nome_sala.strip(),
            "id_sala": id_sala
        }
    except Exception as e:
        print("Erro ao carregar dados do estudante:", e)
        return None
    finally:
        cur.close()
        conn.close()
    

def menu_principal():
    while True:
        clear_screen()
        print("\n===== RPG FGA - MENU INICIAL =====")
        print("1. Selecionar Personagem")
        print("2. Créditos (em breve)")
        print("3. Sair do jogo")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            estudantes = listar_estudantes_disponiveis()
            if not estudantes:
                print("Nenhum estudante disponível.")
                continue
            print("\n🎓 Estudantes disponíveis:")
            for id_, nome in estudantes:
                print(f"ID: {id_} | Nome: {nome}")
            escolhido = input("\nDigite o ID do estudante: ")
            if not escolhido.isdigit():
                print("ID inválido.")
                continue
            jogador = carregar_dados_estudante(int(escolhido))
            if jogador:
                menu_jogador(jogador)
        elif opcao == "2":
            print("\n📜 Créditos: Jogo desenvolvido por Rafael e IA da OpenAI (ChatGPT) 😎")
        elif opcao == "3":
            print("👋 Saindo do jogo...")
            sys.exit()
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    menu_principal()