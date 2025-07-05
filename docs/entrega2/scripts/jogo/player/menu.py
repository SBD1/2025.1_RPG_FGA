from jogo.player.habilidades import *
from jogo.player.inventario import *
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
        print("[1] Ver catálogo de habilidades")
        print("[2] Mudar de sala (em desenvolvimento)")
        print("[3] Explorar (em desenvolvimento)")
        print("[4] Sair para o menu principal")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            habilidades = buscar_habilidades_estudante_todas(jogador['id'])
            mostrar_catalogo_habilidades(habilidades)
            input("\nPressione Enter para voltar ao menu.")
        elif opcao == '2':
            print("➡️ Mudando de sala... (em desenvolvimento)")
        elif opcao == '3':
            print("🔍 Explorando... (em desenvolvimento)")
        elif opcao == '4':
            print("↩️ Retornando ao menu principal.")
            break
        else:
            print("❌ Opção inválida. Tente novamente.")
