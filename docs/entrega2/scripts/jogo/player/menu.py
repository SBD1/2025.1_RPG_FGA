def barra_stamina(stamina, max_stamina=100):
    blocos = int(stamina // 10)
    vazios = 10 - blocos
    return "🟨" * blocos + "⬛" * vazios


def menu_jogador(jogador):
    while True:
        print("\n========= MENU DO JOGADOR =========")
        print(f"🎒 {jogador['nome']} | Stamina: [{barra_stamina(jogador['stamina'])}] {jogador['stamina']}/{jogador['max_stamina']}")
        print("[1] Ver itens")
        print("[2] Ver habilidades")
        print("[3] Mudar de sala")
        print("[4] Explorar")
        print("[5] Voltar")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            print("\n📦 Inventário:")
            for item in jogador['itens']:
                print(f"- {item}")
        elif opcao == '2':
            print("\n🧠 Habilidades:")
            for habilidade in jogador['habilidades']:
                print(f"- {habilidade['nome']} | Tipo: {habilidade['tipo']} | Potência: {habilidade['potencia']}")
        elif opcao == '3':
            print("➡️ Mudando de sala... (a lógica ainda será implementada)")
        elif opcao == '4':
            print("🔍 Explorando a área... (a lógica ainda será implementada)")
        elif opcao == '5':
            print("↩️ Retornando ao menu anterior.")
            break
        else:
            print("❌ Opção inválida. Tente novamente.")



# Simulação de dados do jogador
jogador = {
    "nome": "Estudante Rafael",
    "stamina": 60,
    "max_stamina": 100,
    "itens": ["Poção de Vida", "Livro de FGA", "Moeda de Bronze"],
    "habilidades": [
        {"nome": "Chama Sombria", "tipo": "G", "potencia": 85},
        {"nome": "Benção da Luz", "tipo": "M", "potencia": 80},
    ]
}

# Chamada do menu
menu_jogador(jogador)