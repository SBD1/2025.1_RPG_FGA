from jogo.db import get_db_connection, clear_screen
from jogo.map.dungeon import tem_dungeon_interativo
from jogo.map.loja import acessar_loja
from psycopg2 import Error

def listar_salas(id_estudante=None):
    # Esta função permanece inalterada
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        if id_estudante:
            cur.execute("SELECT id_sala FROM estudante WHERE id_estudante = %s", (id_estudante,))
            sala_atual = cur.fetchone()
            if not sala_atual:
                print("Estudante não encontrado ou sem sala atribuída.")
                return []

            sala_atual_id = sala_atual[0]

            query = """
                SELECT s.id_sala, s.nome, s.descricao, c.nome as campus
                FROM sala_comum s
                JOIN setor st ON s.id_setor = st.id_setor
                JOIN campus c ON st.id_campus = c.id_campus
                WHERE s.id_sala IN (
                    SELECT id_prevSala FROM sala_comum WHERE id_sala = %s
                    UNION
                    SELECT id_proxSala FROM sala_comum WHERE id_sala = %s
                )
                ORDER BY s.id_sala
            """
            cur.execute(query, (sala_atual_id, sala_atual_id))
            salas = cur.fetchall()
            
            salas_corrigidas = [(sala[0], sala[1].strip(), sala[2].strip(), sala[3].strip()) for sala in salas]
            return salas_corrigidas

    except (Exception, Error) as e:
        print("Erro ao listar salas:", e)
        return []

    finally:
        if conn:
            conn.close()


def mover_estudante_para_sala(id_estudante, novo_id_sala):
    # Esta função permanece inalterada
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT e.nome, s.nome FROM Estudante e JOIN Sala_Comum s ON e.id_sala = s.id_sala WHERE e.id_estudante = %s", (id_estudante,))
        estudante = cur.fetchone()
        if not estudante:
            print("Estudante não encontrado.")
            return False

        cur.execute("SELECT nome FROM Sala_Comum WHERE id_sala = %s", (novo_id_sala,))
        nova_sala = cur.fetchone()
        if not nova_sala:
            print("Sala com esse ID não encontrada.")
            return False

        cur.execute("UPDATE Estudante SET id_sala = %s WHERE id_estudante = %s", (novo_id_sala, id_estudante))
        conn.commit()

        print(f"Movido de '{estudante[1].strip()}' para '{nova_sala[0].strip()}' com sucesso!")
        return True

    except (Exception, Error) as e:
        print("Erro ao mover estudante:", e)
        conn.rollback()
        return False

    finally:
        if conn:
            conn.close()

# ======== NOVA FUNÇÃO AUXILIAR ========
def coletar_itens_da_sala(jogador, itens_no_chao, conn, cur):
    """Lida com a lógica de coletar todos os itens encontrados no chão."""
    clear_screen()
    print("Você encontrou os seguintes itens no chão:")
    for _, nome_item in itens_no_chao:
        print(f"- {nome_item.strip()}")

    confirmacao = input("\nDeseja coletar todos os itens? (s/n): ").strip().lower()
    if confirmacao == 's':
        id_estudante = jogador['id']
        itens_coletados = 0
        for id_instancia, nome_item in itens_no_chao:
            # Atualiza a instância do item para pertencer ao jogador e remove da sala
            cur.execute(
                "UPDATE instancia_de_item SET id_estudante = %s, id_sala = NULL WHERE id_instanciaItem = %s",
                (id_estudante, id_instancia)
            )
            print(f"Você coletou: {nome_item.strip()}")
            itens_coletados += 1
        
        if itens_coletados > 0:
            conn.commit()
            print("\nTodos os itens foram adicionados ao seu inventário.")
        else:
            print("\nNenhum item foi coletado.")
    else:
        print("\nVocê deixou os itens no chão.")
    
    input("\nPressione Enter para continuar.")


# ======== FUNÇÃO PRINCIPAL MODIFICADA ========
def explorar_sala(jogador):
    """Verifica o que há na sala e oferece um menu de ações contextuais."""
    clear_screen()
    print("🔍 Explorando a sala...\n")
    id_sala = jogador['id_sala']
    
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # 1. Verifica se tem loja ou dungeon
        cur.execute("SELECT tem_dungeon, tem_loja FROM sala_comum WHERE id_sala = %s", (id_sala,))
        resultado = cur.fetchone()
        tem_dungeon, tem_loja = (False, False) if not resultado else resultado

        # 2. Verifica se há itens no chão
        cur.execute("""
            SELECT
                ii.id_instanciaItem,
                COALESCE(c.nome, e.nome, m.nome) AS nome_item
            FROM instancia_de_item ii
            JOIN tipo_item ti ON ii.id_item = ti.id_item
            LEFT JOIN consumivel c ON ti.id_item = c.id_item
            LEFT JOIN equipavel e ON ti.id_item = e.id_item
            LEFT JOIN monetario m ON ti.id_item = m.id_item
            WHERE ii.id_sala = %s AND ii.id_estudante IS NULL;
        """, (id_sala,))
        itens_no_chao = cur.fetchall()

        print(f"Você está em: {jogador['nome_sala'].strip()}.")
        
        # Monta o menu de opções dinamicamente
        opcoes = {}
        contador_opcoes = 1
        encontrou_algo = False

        if tem_dungeon:
            print("- Você encontrou a entrada de uma Dungeon! 🏰")
            opcoes[str(contador_opcoes)] = ("Entrar na Dungeon", lambda: tem_dungeon_interativo(jogador))
            contador_opcoes += 1
            encontrou_algo = True
        
        if tem_loja:
            print("- Você encontrou uma Loja! 🏪")
            opcoes[str(contador_opcoes)] = ("Acessar Loja", lambda: acessar_loja(jogador))
            contador_opcoes += 1
            encontrou_algo = True
        
        if itens_no_chao:
            print("- Você vê alguns itens no chão! ✨")
            # A função de coleta será uma opção no menu
            opcoes[str(contador_opcoes)] = ("Coletar Itens", lambda: coletar_itens_da_sala(jogador, itens_no_chao, conn, cur))
            contador_opcoes += 1
            encontrou_algo = True

        if not encontrou_algo:
            print("\nNão há nada de especial por aqui. Apenas o vazio da vida acadêmica.")
            input("\nPressione Enter para voltar.")
            return

        # Exibe o menu de ações
        print("\nO que você deseja fazer?")
        for key, (texto, _) in opcoes.items():
            print(f"[{key}] {texto}")
        print(f"[{contador_opcoes}] Voltar")

        while True:
            escolha = input("\nEscolha uma opção: ").strip()

            if escolha in opcoes:
                texto_acao, acao = opcoes[escolha]
                acao()  # Executa a função associada
                # Após a ação, o loop é quebrado para voltar ao menu principal
                break 
            elif escolha == str(contador_opcoes):
                print("Voltando ao menu...")
                break
            else:
                print("❌ Opção inválida. Tente novamente.")
    
    except (Exception, Error) as e:
        if conn:
            conn.rollback()
        print(f"❌ Erro ao explorar a sala: {e}")
        input("\nPressione Enter para continuar.")
    finally:
        if conn:
            conn.close()
