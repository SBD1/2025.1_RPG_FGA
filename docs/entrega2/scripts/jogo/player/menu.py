from jogo.player.habilidades import *
from jogo.player.afinidade import *
from jogo.player.inventario import *
from jogo.map.sala import *
from jogo.map.setor import *
from jogo.db import clear_screen
from jogo.player.estresse import *

def carregar_estudante(id_estudante):
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

def barra_estresse(estresse, max_estresse=100):
    blocos = int((estresse / max_estresse) * 10)
    blocos = min(blocos, 10)
    vazios = 10 - blocos
    return "🟧" * blocos + "⬛" * vazios

# ======== FUNÇÃO MODIFICADA E SIMPLIFICADA ========
def menu_jogador(jogador):
    while True:

        jogador.update(carregar_estudante(jogador['id']))
        verifica_estresse(jogador)
        input("\nPressione Enter para continuar.")


        clear_screen()
        print("\n========= MENU DO JOGADOR =========")
        print(f"🎒 {jogador['nome']} | Estresse: [{barra_estresse(jogador['estresse'])}] {jogador['estresse']}/100")
        print(f"💰 Dinheiro: {jogador['total_dinheiro']}")
        print(f"📍 Sala atual: {jogador['nome_sala']}")
        print("\n[1] Ver catálogo de habilidades")
        print("[2] Mudar de sala")
        print("[3] Mudar de setor")
        print("[4] Explorar sala atual") # <<-- Ação principal
        print("[5] Ver afinidades")
        print("[6] Sair para o menu principal") # <<-- Menu mais enxuto

        opcao = input("\nEscolha uma opção: ")

        if opcao == '1':
            clear_screen()
            habilidades = buscar_habilidades_estudante_todas(jogador['id'])
            mostrar_catalogo_habilidades(habilidades)
            input("\nPressione Enter para voltar ao menu.")
        
        elif opcao == '2':
            clear_screen()
            salas = listar_salas(jogador['id'])
            if not salas:
                print("❌ Nenhuma sala vizinha disponível.")
            else:
                print("\nSalas vizinhas:")
                for sala in salas:
                    print(f"ID: {sala[0]} | Nome: {sala[1]} | Campus: {sala[3]}\n   Descrição: {sala[2]}")
                try:
                    novo_id = int(input("\nDigite o ID da sala para onde deseja ir: "))
                    sucesso = mover_estudante_para_sala(jogador['id'], novo_id)
                    if sucesso:
                        for sala in salas:
                            if sala[0] == novo_id:
                                jogador['id_sala'] = novo_id  
                                jogador['nome_sala'] = sala[1]
                                break
                except ValueError:
                    print("❌ Entrada inválida.")
            input("\nPressione Enter para continuar.")

        elif opcao == '3':
            clear_screen()
            nova_sala = mudar_setor_estudante(jogador['id'])
            if nova_sala:
                jogador['nome_sala'] = nova_sala
            input("\nPressione Enter para continuar.")

        elif opcao == '4':
            # Agora esta função lida com a lógica de loja/dungeon
            explorar_sala(jogador)
            # A função explorar_sala já pede um input, então não é necessário aqui.

        elif opcao == '5':
            clear_screen()
            mostrar_menu_afinidade(jogador)
            input("\nPressione Enter para continuar.")

        elif opcao == '6':
            print("↩️ Retornando ao menu principal.")
            break

        else:
            print("❌ Opção inválida. Tente novamente.")
            input("\nPressione Enter para tentar novamente.")