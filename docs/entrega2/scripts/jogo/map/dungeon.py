from jogo.db import *
from jogo.monster.boss import *
from jogo.monster.monster import *

def sala_tem_dungeon(id_sala):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT 1 FROM dungeon_academica WHERE id_dungeon = %s
        """, (id_sala,))
        return cur.fetchone() is not None

    except Exception as e:
        print(f"Erro ao verificar dungeon na sala: {e}")
        return False

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def mostrar_boss_e_monstros(id_sala):
    clear_screen()

    boss_reliquia = buscar_boss_e_reliquia(id_sala)
    if not boss_reliquia:
        print("Erro: dungeon sem boss.")
        input("\nPressione Enter para voltar.")
        return

    (id_criatura, nome_boss, descricao_boss, nivel, vida_max, id_reliquia,
     nome_reliquia, desc_reliquia, tipo_reliquia, id_instanciaCriatura, vida_atual) = boss_reliquia

    print(f"🦹 Boss: {nome_boss} (Nível {nivel})")
    print(f"Descrição: {descricao_boss}")
    print(f"Vida: {vida_atual}/{vida_max}")
    print(f"Tipo de relíquia: {tipo_reliquia}\n")

    monstros_simples = buscar_monstros_simples(id_sala)
    print("👾 Monstros Simples na Dungeon:\n")
    if not monstros_simples:
        print("Nenhum monstro simples encontrado.")
    else:
        for idx, m in enumerate(monstros_simples, start=1):
            (id_c, nome, descricao, nivel_m, vida_max_m, xp_tema, qtd_moedas, id_instancia, vida_atual_m) = m
            print(f"[{idx}] {nome} (Nível {nivel_m}) - Vida: {vida_atual_m}/{vida_max_m}")
            print(f"    Descrição: {descricao}\n")

        print("[0] Voltar")

        escolha = input("Escolha o monstro para enfrentar (digite o número): ")
        if escolha.isdigit():
            escolha = int(escolha)
            if escolha == 0:
                print("Voltando...")
                return
            elif 1 <= escolha <= len(monstros_simples):
                monstro = monstros_simples[escolha-1]
                print(f"Você escolheu enfrentar {monstro[1]}!")
                input("\nPressione Enter para continuar (implementação do combate).")
            else:
                print("Opção inválida.")
        else:
            print("Entrada inválida.")


def tem_dungeon(jogador):
    id_sala = jogador['id_sala']
    id_estudante = jogador['id']

    if not sala_tem_dungeon(id_sala):
        return False  # Agora verifica corretamente se há dungeon

    boss_reliquia = buscar_boss_e_reliquia(id_sala)
    if not boss_reliquia:
        print("⚠️ Dungeon existe, mas não foi encontrado o boss.")
        return True  # Dungeon existe, mas incompleta

    (id_criatura, nome_boss, descricao_boss, nivel, vida_max, id_reliquia,
     nome_reliquia, desc_reliquia, tipo_reliquia, id_instanciaCriatura, vida_atual) = boss_reliquia

    tem_reliquia = jogador_tem_reliquia(id_estudante, id_reliquia)
    status = "Fechada (Você já completou esta dungeon)" if tem_reliquia else "Aberta"

    print(f"Dungeon: {nome_reliquia}")
    print(f"Descrição: {desc_reliquia}")
    print(f"Status: {status}\n")

    if tem_reliquia:
        print("Você já concluiu essa dungeon e não pode mais acessá-la.")
        input("\nPressione Enter para voltar.")
        return True

    print("Opções:")
    print("[1] Ver detalhes da dungeon (Boss e monstros)")
    print("[2] Voltar")

    escolha = input("Escolha uma opção: ")

    if escolha == '1':
        mostrar_boss_e_monstros(id_sala)
    else:
        print("Voltando...")

    return True


def jogador_tem_reliquia(id_estudante, id_reliquia):
    """Verifica se o jogador já possui a relíquia (indicando que finalizou a dungeon)."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        query = """
            SELECT 1 FROM inventario
            WHERE id_estudante = %s AND id_item = %s
            LIMIT 1;
        """
        cur.execute(query, (id_estudante, id_reliquia))
        return cur.fetchone() is not None
    except Exception as e:
        print(f"Erro ao verificar relíquia do jogador: {e}")
        return False
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
