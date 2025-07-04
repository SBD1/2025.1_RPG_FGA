def barra_vida(vida, nome):
    blocos = int(vida // 20)
    vazios = 10 - blocos
    barra = "🟥" * blocos + "⬛" * vazios
    print(f"{nome}: [{barra}] {vida:.0f}/200")

def menu(vida_jogador, vida_monstro):
    print('\n=========== COMBATE MORTAL ===========')
    barra_vida(vida_jogador, "🧙 Jogador")
    barra_vida(vida_monstro, "👹 Monstro")
    print('Escolha o que deseja realizar:')
    print('[A] Habilidade de Ataque')
    print('[D] Habilidade de Defesa')
    print('[C] Habilidade de Cura')
    print('[F] Fugir')

def lista_habilidades(categoria_dict):
    for i, (nome, detalhes) in enumerate(categoria_dict.items(), 1):
        print(f"[{i}] {nome} | Tipo: {detalhes['tipo']} | Potência: {detalhes['potencia']}")

def escolher_habilidade(categoria, habilidades):
    habilidades_categoria = list(habilidades[categoria].items())
    lista_habilidades(habilidades[categoria])
    while True:
        try:
            escolha = int(input("Escolha a habilidade [1-4]: ")) - 1
            if 0 <= escolha < len(habilidades_categoria):
                return habilidades_categoria[escolha]
        except ValueError:
            pass
        print("Opção inválida. Tente novamente.")
