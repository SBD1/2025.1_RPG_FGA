# jogo/debug_menu.py

from .db import get_db_connection, clear_screen
from psycopg2 import Error

def listar_salas_com_dungeon():
    """Consulta e exibe todas as salas que possuem uma dungeon."""
    clear_screen()
    print("--- 🏰 Salas com Dungeon ---")
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT s.id_sala, s.nome, st.nome AS nome_setor
            FROM sala_comum s
            JOIN setor st ON s.id_setor = st.id_setor
            WHERE s.tem_dungeon = TRUE
            ORDER BY s.id_sala;
        """)
        salas = cur.fetchall()

        if not salas:
            print("Nenhuma sala com dungeon encontrada.")
        else:
            print(f"{'ID da Sala':<12} | {'Nome da Sala':<30} | {'Setor'}")
            print("-" * 60)
            for sala in salas:
                print(f"{sala[0]:<12} | {sala[1].strip():<30} | {sala[2].strip()}")
        
        cur.close()
        conn.close()
    except (Exception, Error) as e:
        print(f"Erro ao buscar salas com dungeon: {e}")

    input("\nPressione Enter para voltar...")

def listar_salas_com_loja():
    """Consulta e exibe todas as salas que possuem uma loja."""
    clear_screen()
    print("--- 🏪 Salas com Loja ---")
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT s.id_sala, s.nome, st.nome AS nome_setor
            FROM sala_comum s
            JOIN setor st ON s.id_setor = st.id_setor
            WHERE s.tem_loja = TRUE
            ORDER BY s.id_sala;
        """)
        salas = cur.fetchall()

        if not salas:
            print("Nenhuma sala com loja encontrada.")
        else:
            print(f"{'ID da Sala':<12} | {'Nome da Sala':<30} | {'Setor'}")
            print("-" * 60)
            for sala in salas:
                print(f"{sala[0]:<12} | {sala[1].strip():<30} | {sala[2].strip()}")

        cur.close()
        conn.close()
    except (Exception, Error) as e:
        print(f"Erro ao buscar salas com loja: {e}")

    input("\nPressione Enter para voltar...")

def listar_salas_com_itens():
    """Consulta e exibe todas as salas que possuem itens no chão."""
    clear_screen()
    print("--- ✨ Salas com Itens no Chão ---")
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT s.id_sala, s.nome, COUNT(ii.id_instanciaItem) AS quantidade_itens
            FROM sala_comum s
            JOIN instancia_de_item ii ON s.id_sala = ii.id_sala
            WHERE ii.id_estudante IS NULL
            GROUP BY s.id_sala, s.nome
            ORDER BY s.id_sala;
        """)
        salas = cur.fetchall()

        if not salas:
            print("Nenhuma sala com itens no chão encontrada.")
        else:
            print(f"{'ID da Sala':<12} | {'Nome da Sala':<30} | {'Qtd. de Itens'}")
            print("-" * 60)
            for sala in salas:
                print(f"{sala[0]:<12} | {sala[1].strip():<30} | {sala[2]}")

        cur.close()
        conn.close()
    except (Exception, Error) as e:
        print(f"Erro ao buscar salas com itens: {e}")

    input("\nPressione Enter para voltar...")

def listar_posicao_jogadores():
    """Consulta e exibe a localização atual de todos os jogadores."""
    clear_screen()
    print("--- 📍 Posição dos Jogadores ---")
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT
                e.nome AS nome_jogador,
                s.nome AS nome_sala,
                st.nome AS nome_setor
            FROM estudante e
            JOIN sala_comum s ON e.id_sala = s.id_sala
            JOIN setor st ON s.id_setor = st.id_setor
            ORDER BY e.id_estudante;
        """)
        jogadores = cur.fetchall()

        if not jogadores:
            print("Nenhum jogador encontrado no banco de dados.")
        else:
            print(f"{'Jogador':<20} | {'Sala Atual':<30} | {'Setor'}")
            print("-" * 70)
            for jogador in jogadores:
                print(f"{jogador[0].strip():<20} | {jogador[1].strip():<30} | {jogador[2].strip()}")

        cur.close()
        conn.close()
    except (Exception, Error) as e:
        print(f"Erro ao buscar a posição dos jogadores: {e}")

    input("\nPressione Enter para voltar...")

# ======== NOVA FUNÇÃO ========
def listar_detalhes_dungeons():
    """Consulta e exibe informações detalhadas de todas as dungeons."""
    clear_screen()
    print("--- 📜 Detalhes das Dungeons ---")
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        # A query que você pediu, mas sem o WHERE para listar todas
        cur.execute("""
            SELECT
                s.id_sala,
                s.nome AS nome_sala,
                d.nome AS nome_dungeon,
                t.nome AS nome_tema
            FROM
                sala_comum s
            JOIN
                dungeon_academica d ON d.id_dungeon = s.id_sala
            JOIN
                tema t ON d.id_tema = t.id_tema
            ORDER BY
                s.id_sala;
        """)
        dungeons = cur.fetchall()

        if not dungeons:
            print("Nenhuma dungeon encontrada no banco de dados.")
        else:
            print(f"{'ID Sala':<10} | {'Nome da Sala':<25} | {'Nome da Dungeon':<30} | {'Tema'}")
            print("-" * 90)
            for dungeon in dungeons:
                # id_sala, nome_sala, nome_dungeon, nome_tema
                print(f"{dungeon[0]:<10} | {dungeon[1].strip():<25} | {dungeon[2].strip():<30} | {dungeon[3].strip()}")

        cur.close()
        conn.close()
    except (Exception, Error) as e:
        print(f"Erro ao buscar detalhes das dungeons: {e}")

    input("\nPressione Enter para voltar...")


def adicionar_moedas_a_jogador():
    """Permite escolher um jogador e adicionar moedas ao saldo atual (total_dinheiro)."""
    clear_screen()
    print("--- 💰 Adicionar Dinheiro a um Jogador ---")
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Lista jogadores
        cur.execute("""
            SELECT e.id_estudante, e.nome, e.total_dinheiro, s.nome AS nome_sala
            FROM estudante e
            JOIN sala_comum s ON e.id_sala = s.id_sala
            ORDER BY e.id_estudante;
        """)
        jogadores = cur.fetchall()

        if not jogadores:
            print("Nenhum jogador encontrado.")
            return

        print(f"{'ID':<5} | {'Nome':<25} | {'Sala':<25} | {'Dinheiro'}")
        print("-" * 70)
        for j in jogadores:
            print(f"{j[0]:<5} | {j[1].strip():<25} | {j[3].strip():<25} | {j[2]}")

        id_escolhido = input("\nDigite o ID do jogador para adicionar dinheiro (ou 0 para cancelar): ").strip()
        if not id_escolhido.isdigit() or int(id_escolhido) == 0:
            print("Cancelado.")
            return

        id_escolhido = int(id_escolhido)
        jogador = next((j for j in jogadores if j[0] == id_escolhido), None)

        if not jogador:
            print("Jogador não encontrado.")
            return

        qtd = input("Digite a quantidade de dinheiro a adicionar (1 a 200): ").strip()
        if not qtd.isdigit():
            print("Entrada inválida.")
            return

        qtd = int(qtd)
        if qtd < 1 or qtd > 200:
            print("A quantidade deve estar entre 1 e 200.")
            return

        novo_saldo = jogador[2] + qtd
        cur.execute("""
            UPDATE estudante
            SET total_dinheiro = %s
            WHERE id_estudante = %s
        """, (novo_saldo, id_escolhido))

        conn.commit()
        print(f"✅ R${qtd},00 adicionados com sucesso ao jogador {jogador[1].strip()} (Novo saldo: R${novo_saldo},00)")

    except Exception as e:
        print(f"❌ Erro ao adicionar dinheiro: {e}")
    finally:
        if conn:
            conn.close()

    input("\nPressione Enter para voltar...")

def menu_debug_queries():
    """Exibe o menu de consultas de debug."""
    while True:
        clear_screen()
        print("\n--- 🛠️  Menu de Consultas de Debug 🛠️  ---")
        print("[1] Listar salas com Dungeon")
        print("[2] Listar salas com Loja")
        print("[3] Listar salas com Itens no Chão")
        print("[4] Mostrar Posição dos Jogadores")
        print("[5] Ver Detalhes das Dungeons") 
        print("[6] Adicionar Moedas a Jogador") 
        print("[7] Voltar ao Menu Principal")  
        
        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == '1':
            listar_salas_com_dungeon()
        elif opcao == '2':
            listar_salas_com_loja()
        elif opcao == '3':
            listar_salas_com_itens()
        elif opcao == '4':
            listar_posicao_jogadores()
        elif opcao == '5': # <<-- NOVA CONDIÇÃO
            listar_detalhes_dungeons()
        elif opcao == '6':
            adicionar_moedas_a_jogador()
        elif opcao == '7':
            print("Retornando ao menu principal...")
            break
        else:
            print("Opção inválida.")
            input("\nPressione Enter para tentar novamente.")