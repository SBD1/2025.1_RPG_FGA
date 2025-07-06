from jogo.db import get_db_connection, clear_screen
from psycopg2 import Error

def exibir_itens_e_habilidades(id_loja, cur):
    """Exibe os itens e habilidades disponíveis na loja, buscando os preços corretamente."""
    
    # Query para buscar APENAS consumíveis à venda
    cur.execute("""
        SELECT i.id_item, c.nome, c.descricao, c.preco
        FROM loja_item li
        JOIN tipo_item i ON li.id_item = i.id_item
        JOIN consumivel c ON i.id_item = c.id_item
        WHERE li.id_sala = %s;
    """, (id_loja,))
    itens = cur.fetchall()

    # Query corrigida para buscar o preço das tabelas de habilidade específicas
    cur.execute("""
        SELECT 
            th.id_habilidade, 
            COALESCE(a.nome, c.nome, d.nome) AS nome,
            th.tipo_habilidade,
            COALESCE(a.preco, c.preco, d.preco) AS preco
        FROM habilidade_loja hl
        JOIN tipoHabilidade th ON hl.id_habilidade = th.id_habilidade
        LEFT JOIN Ataque a ON hl.id_habilidade = a.id_habilidade
        LEFT JOIN Cura c ON hl.id_habilidade = c.id_habilidade
        LEFT JOIN Defesa d ON hl.id_habilidade = d.id_habilidade
        WHERE hl.id_loja = %s;
    """, (id_loja,))
    habilidades = cur.fetchall()

    clear_screen()
    print("="*80)
    print("🏪 BEM-VINDO À LOJA! 🏪".center(80))
    print("="*80)

    if not itens and not habilidades:
        print("\nEsta loja está vazia no momento.")
        return [], []

    print("\n--- ITENS CONSUMÍVEIS À VENDA ---")
    if not itens:
        print("Nenhum item disponível.")
    else:
        print(f"{'ID':<5} {'Nome':<30} {'Preço':<10} {'Descrição'}")
        print("-"*80)
        for item in itens:
            # id_item, nome, descricao, preco
            print(f"{item[0]:<5} {item[1].strip():<30} {item[3]:<10} {item[2].strip()}")

    print("\n--- HABILIDADES À VENDA ---")
    if not habilidades:
        print("Nenhuma habilidade disponível.")
    else:
        print(f"{'ID':<5} {'Nome':<30} {'Tipo':<15} {'Preço'}")
        print("-"*80)
        for hab in habilidades:
            # id_habilidade, nome, tipo, preco
            if hab[3] is None: # Checa se o preço é nulo (habilidade pode não ter preço definido)
                continue
            print(f"{hab[0]:<5} {hab[1].strip():<30} {hab[2].strip():<15} {hab[3]}")

    print("="*80)
    return itens, habilidades

def comprar_item(jogador, item, conn, cur):
    """Realiza a compra de um item."""
    id_estudante = jogador['id']
    id_item, nome_item, _, preco_item = item

    if jogador['total_dinheiro'] < preco_item:
        print("❌ Dinheiro insuficiente!")
        return

    # Deduz o dinheiro
    nova_quantia = jogador['total_dinheiro'] - preco_item
    cur.execute("UPDATE estudante SET total_dinheiro = %s WHERE id_estudante = %s", (nova_quantia, id_estudante))

    # Adiciona o item ao inventário do estudante
    cur.execute("INSERT INTO instancia_de_item (id_estudante, id_item) VALUES (%s, %s)", (id_estudante, id_item))

    conn.commit()
    jogador['total_dinheiro'] = nova_quantia
    print(f"✅ Você comprou {nome_item.strip()}!")

def comprar_habilidade(jogador, habilidade, conn, cur):
    """Realiza a compra de uma habilidade."""
    id_estudante = jogador['id']
    id_habilidade, nome_habilidade, _, preco_habilidade = habilidade

    if jogador['total_dinheiro'] < preco_habilidade:
        print("❌ Dinheiro insuficiente!")
        return

    # Verifica se o jogador já possui a habilidade
    cur.execute("SELECT 1 FROM habilidade_estudante WHERE id_estudante = %s AND id_habilidade = %s", (id_estudante, id_habilidade))
    if cur.fetchone():
        print("❌ Você já possui esta habilidade.")
        return

    # Deduz o dinheiro
    nova_quantia = jogador['total_dinheiro'] - preco_habilidade
    cur.execute("UPDATE estudante SET total_dinheiro = %s WHERE id_estudante = %s", (nova_quantia, id_estudante))

    # Adiciona a habilidade ao jogador
    cur.execute("INSERT INTO habilidade_estudante (id_estudante, id_habilidade) VALUES (%s, %s)", (id_estudante, id_habilidade))

    conn.commit()
    jogador['total_dinheiro'] = nova_quantia
    print(f"✅ Você aprendeu a habilidade {nome_habilidade.strip()}!")

def acessar_loja(jogador):
    """Função principal para acessar e interagir com a loja."""
    id_sala = jogador['id_sala']
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT tem_loja FROM sala_comum WHERE id_sala = %s", (id_sala,))
        resultado = cur.fetchone()

        if not resultado or not resultado[0]:
            print("\nEsta sala não possui uma loja.")
            input("\nPressione Enter para voltar.")
            return

        id_loja = id_sala 

        while True:
            itens, habilidades = exibir_itens_e_habilidades(id_loja, cur)
            print(f"\nSeu dinheiro: {jogador['total_dinheiro']} 💰")
            print("\nOpções:")
            print("[I] Comprar Item")
            print("[H] Comprar Habilidade")
            print("[S] Sair da Loja")
            escolha = input("Escolha uma opção: ").strip().upper()

            if escolha == 'S':
                print("👋 Até mais!")
                break
            
            elif escolha == 'I':
                if not itens:
                    print("Não há itens para comprar.")
                else:
                    try:
                        id_compra = int(input("Digite o ID do item que deseja comprar: "))
                        item_selecionado = next((item for item in itens if item[0] == id_compra), None)
                        if item_selecionado:
                            comprar_item(jogador, item_selecionado, conn, cur)
                        else:
                            print("ID de item inválido.")
                    except ValueError:
                        print("Entrada inválida.")
                input("\nPressione Enter para continuar.")

            elif escolha == 'H':
                if not habilidades:
                    print("Não há habilidades para comprar.")
                else:
                    try:
                        id_compra = int(input("Digite o ID da habilidade que deseja comprar: "))
                        habilidade_selecionada = next((hab for hab in habilidades if hab[0] == id_compra), None)
                        if habilidade_selecionada:
                            comprar_habilidade(jogador, habilidade_selecionada, conn, cur)
                        else:
                            print("ID de habilidade inválido.")
                    except ValueError:
                        print("Entrada inválida.")
                input("\nPressione Enter para continuar.")
                
            else:
                print("Opção inválida.")
                input("\nPressione Enter para tentar novamente.")

    except (Exception, Error) as e:
        if conn:
            conn.rollback()
        print(f"❌ Erro ao acessar a loja: {e}")
        input("\nPressione Enter para voltar.")
    finally:
        if conn:
            conn.close()