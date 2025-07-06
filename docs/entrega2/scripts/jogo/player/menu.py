from jogo.player.habilidades import *
from jogo.player.inventario import *
from jogo.map.sala import *
from jogo.map.setor import *
from jogo.map.dungeon import *
from jogo.db import clear_screen

def barra_estresse(estresse, max_estresse=100):
    blocos = int((estresse / max_estresse) * 10)
    blocos = min(blocos, 10)
    vazios = 10 - blocos
    return "🟧" * blocos + "⬛" * vazios

def menu_jogador(jogador):
    while True:
        clear_screen()
        print("\n========= MENU DO JOGADOR =========")
        print(f"🎒 {jogador['nome']} | Estresse: [{barra_estresse(jogador['estresse'])}] {jogador['estresse']}/100")
        print(f"💰 Dinheiro: {jogador['total_dinheiro']}")
        print(f"📍 Sala atual: {jogador['nome_sala']}")
        print("\n[1] Ver catálogo de habilidades")
        print("[2] Mudar de sala")
        print("[3] Mudar de setor")
        print("[4] Explorar (em desenvolvimento)")
        print("[5] Sair para o menu principal")

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
            clear_screen()
            explorar_sala(jogador)
            input("\nPressione Enter para continuar.")

        elif opcao == '5':
            print("↩️ Retornando ao menu principal.")
            break

        else:
            print("❌ Opção inválida. Tente novamente.")
            input("\nPressione Enter para tentar novamente.")
