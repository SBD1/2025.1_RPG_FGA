from jogo.db import get_db_connection
from jogo.db import clear_screen
from jogo.player.equipar import *
from jogo.player.consumir import *

def buscar_consumiveis(id_estudante):
    query = """
    SELECT ci.id_instanciaItem,
           c.nome AS nome_item,
           c.descricao,
           c.efeito,
           c.preco
    FROM instancia_de_item ci
    JOIN consumivel c ON ci.id_item = c.id_item
    WHERE ci.id_estudante = %s;
    """
    conn = None
    consumiveis = []
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute(query, (id_estudante,))
            rows = cur.fetchall()
            for row in rows:
                consumiveis.append({
                    'id_instanciaItem': row[0],
                    'nome_item': row[1],
                    'descricao': row[2],
                    'efeito': row[3],
                    'preco': row[4]
                })
    except Exception as e:
        print(f"Erro ao buscar consumíveis: {e}")
    finally:
        if conn:
            conn.close()
    return consumiveis



def buscar_equipaveis(id_estudante):
    query = """
    SELECT ei.id_instanciaItem,
           e.nome AS nome_item,
           e.descricao,
           e.efeito,
           e.preco,
           ei.equipado
    FROM instancia_de_item ei
    JOIN equipavel e ON ei.id_item = e.id_item
    WHERE ei.id_estudante = %s;
    """
    conn = None
    equipaveis = []
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute(query, (id_estudante,))
            rows = cur.fetchall()
            for row in rows:
                equipaveis.append({
                    'id_instanciaItem': row[0],
                    'nome_item': row[1],
                    'descricao': row[2],
                    'efeito': row[3],
                    'preco': row[4],
                    'equipado': row[5]
                })
    except Exception as e:
        print(f"Erro ao buscar equipáveis: {e}")
    finally:
        if conn:
            conn.close()
    return equipaveis


def buscar_reliquias(id_estudante):
    query = """
    SELECT ri.id_instanciaItem,
           r.nome AS nome_reliquia,
           r.descricao,
           r.tipo_reliquia
    FROM instancia_de_item ri
    JOIN reliquia r ON ri.id_item = r.id_reliquia
    WHERE ri.id_estudante = %s;
    """
    conn = None
    reliquias = []
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute(query, (id_estudante,))
            rows = cur.fetchall()
            for row in rows:
                reliquias.append({
                    'id_instanciaItem': row[0],
                    'nome_reliquia': row[1],
                    'descricao': row[2],
                    'tipo_reliquia': row[3]
                })
    except Exception as e:
        print(f"Erro ao buscar relíquias: {e}")
    finally:
        if conn:
            conn.close()
    return reliquias


def buscar_monetarios(id_estudante):
    query = """
    SELECT mi.id_instanciaItem,
           m.nome AS nome_item,
           m.descricao,
           m.valor
    FROM instancia_de_item mi
    JOIN monetario m ON mi.id_item = m.id_item
    WHERE mi.id_estudante = %s;
    """
    conn = None
    monetarios = []
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute(query, (id_estudante,))
            rows = cur.fetchall()
            for row in rows:
                monetarios.append({
                    'id_instanciaItem': row[0],
                    'nome_item': row[1],
                    'descricao': row[2],
                    'valor': row[3],
                })
    except Exception as e:
        print(f"Erro ao buscar itens monetários: {e}")
    finally:
        if conn:
            conn.close()
    return monetarios

def mostrar_itens_categoria(itens, categoria, jogador=None):
    if not itens:
        print(f"\n📦 Nenhum item encontrado na categoria {categoria}.")
        return

    print("\n" + "=" * 100)
    print(f"🎒 INVENTÁRIO - {categoria.upper()} 🎒".center(100))
    print("=" * 100)

    for item in itens:
        if categoria == 'Consumíveis':
            print(f"ID: {item['id_instanciaItem']} | Nome: {item['nome_item'].strip()} | Efeito: {item['efeito']} | Descrição: {item['descricao'].strip()}")

        elif categoria == 'Equipáveis':
            status = "✅" if item['equipado'] else "❌"
            print(f"ID: {item['id_instanciaItem']} | Nome: {item['nome_item'].strip()} | Efeito: {item['efeito']} | Descrição: {item['descricao'].strip()} | Equipado: {status}")

        elif categoria == 'Relíquias':
            print(f"ID: {item['id_instanciaItem']} | Nome: {item['nome_reliquia'].strip()} | Tipo: {item['tipo_reliquia'].strip()} | Descrição: {item['descricao'].strip()}")

        elif categoria == 'Monetários':
            print(f"ID: {item['id_instanciaItem']} | Nome: {item['nome_item'].strip()} | Valor: {item['valor']} | Descrição: {item['descricao'].strip()}")
    
    if categoria == 'Consumíveis' and itens:
        print("\n⚡ Ações")
        print("[1] Consumir um item")
        print("[2] Voltar")
        opcao = input("\nEscolha uma ação: ")

        if opcao == '1':
            try:
                id_item = int(input('Informe o ID do item que deseja consumir: '))
                consumir_item(id_item, jogador['id'])
            except ValueError:
                print("❌ ID inválido. Por favor, informe um número válido.")
            
        elif opcao == '2':
            return


    if categoria == 'Equipáveis' and itens:
        print("\n⚡ Ações")
        print("[1] Equipar/Desequipar um item")
        print("[2] Voltar")
        opcao = input("\nEscolha uma ação: ")

        if opcao == '1':
            try:
                id_escolhido = int(input('🔄 Informe o ID do item que deseja equipar/desequipar: '))
                # Procura o item na lista
                item_selecionado = next((i for i in itens if i['id_instanciaItem'] == id_escolhido), None)
                if not item_selecionado:
                    print("❌ ID inválido. Nenhum item encontrado com esse ID.")
                else:
                    # Alterna o status: se estava equipado, desequipa; se não, equipa
                    novo_status = not item_selecionado['equipado']
                    atualizar_status_equipavel(id_escolhido)
            except ValueError:
                print("❌ Entrada inválida. Por favor, informe um número.")
            # input("\nPressione Enter para voltar.")
        elif opcao == '2':
            return


    print("=" * 100)

def menu_inventario(jogador):
    while True:
        clear_screen()
        print("\n🎒 INVENTÁRIO 🎒")
        print("[1] Consumíveis")
        print("[2] Equipáveis")
        print("[3] Relíquias")
        print("[4] Monetários")
        print("[5] Voltar")
        opcao = input("\nEscolha uma categoria: ")

        if opcao == '1':
            clear_screen()
            itens = buscar_consumiveis(jogador['id'])
            mostrar_itens_categoria(itens, 'Consumíveis', jogador)
            input("\nPressione Enter para voltar.")
        elif opcao == '2':
            clear_screen()
            itens = buscar_equipaveis(jogador['id'])
            mostrar_itens_categoria(itens, 'Equipáveis')
            input("\nPressione Enter para voltar.")
        elif opcao == '3':
            clear_screen()
            itens = buscar_reliquias(jogador['id'])
            mostrar_itens_categoria(itens, 'Relíquias')
            input("\nPressione Enter para voltar.")
        elif opcao == '4':
            clear_screen()
            itens = buscar_monetarios(jogador['id'])
            mostrar_itens_categoria(itens, 'Monetários')
            input("\nPressione Enter para voltar.")
        elif opcao == '5':
            break
        else:
            print("❌ Opção inválida.")
            input("\nPressione Enter para tentar novamente.")