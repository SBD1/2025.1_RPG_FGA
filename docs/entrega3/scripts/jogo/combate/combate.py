def barra_vida(vida_atual, vida_maxima, nome):
    total_blocos = 20  # mais suave visualmente
    proporcao = vida_atual / vida_maxima if vida_maxima > 0 else 0
    blocos_cheios = int(proporcao * total_blocos)
    blocos_vazios = total_blocos - blocos_cheios
    barra = "🟥" * blocos_cheios + "⬛" * blocos_vazios
    print(f"{nome}: [{barra}] {vida_atual:.0f}/{vida_maxima}")

def menu(vida_jogador, vida_monstro, vida_max_jogador, vida_max_monstro):
    print('\n============== HORA DO DUELO ==============')
    barra_vida(vida_jogador, vida_max_jogador, "🧙 Jogador")
    barra_vida(vida_monstro, vida_max_monstro, "👹 Monstro")
    print('Escolha o que deseja realizar:')
    print('[A] Habilidade de Ataque')
    print('[D] Habilidade de Defesa')
    print('[C] Habilidade de Cura')
    print('[P] Passar o turno')
    print('[F] Fugir')
    print('===========================================')

def lista_habilidades_com_cooldown(habilidades_dict, cooldowns):
    tipo_emojis = {
        "M": "📐", "P": "💻", "E": "⚙️", "H": "📚", "G": "🌐"
    }
    tipo_nome = {
        "M": "Matemática", "P": "Programação", "E": "Engenharias",
        "H": "Humanidades", "G": "Gerais"
    }

    habilidades_lista = list(habilidades_dict.items())
    for i, (nome, detalhes) in enumerate(habilidades_lista, 1):
        tipo = detalhes["tipo"]
        potencia = detalhes["potencia"]
        cooldown = cooldowns.get(nome, 0)
        emoji = tipo_emojis.get(tipo, "❓")
        nome_tema = tipo_nome.get(tipo, "Desconhecido")
        status = f"(⏳ {cooldown} turno(s))" if cooldown > 0 else ""
        print(f"[{i}] {nome:<25} | Potência: {potencia:<3} | Tema: {emoji} {nome_tema:<12} {status}")

def escolher_habilidade(categoria, habilidades, cooldowns, vida_jogador, vida_monstro):
    print('\n====================== MENU DE ' + f"{categoria.upper()}".ljust(20) + '======================')

    habilidades_categoria = habilidades.get(categoria, {})
    lista_habilidades_com_cooldown(habilidades_categoria, cooldowns)

    disponiveis = [
        (nome, det) for nome, det in habilidades_categoria.items()
        if cooldowns.get(nome, 0) == 0
    ]

    print("\n📊 Vida atual:")
    print(f"🧙 Jogador: {vida_jogador:.0f}/{vida_jogador if vida_jogador > 0 else 1}")  # evitar div/0
    print(f"👹 Monstro: {vida_monstro:.0f}/{vida_monstro if vida_monstro > 0 else 1}")
    print('===========================================================================')

    if not disponiveis:
        print("⏳ Todas as habilidades dessa categoria estão em cooldown.")
        while True:
            escolha = input("Deseja passar o turno? (S/N): ").strip().upper()
            if escolha == 'S':
                return None, None  # sinaliza passar o turno
            elif escolha == 'N':
                return escolher_habilidade(categoria, habilidades, cooldowns, vida_jogador, vida_monstro)
            else:
                print("Opção inválida, digite S ou N.")
    
    while True:
        try:
            escolha = int(input("Escolha a habilidade [número]: ")) - 1
            if 0 <= escolha < len(disponiveis):
                return disponiveis[escolha]
            else:
                print("Opção inválida. Tente novamente.")
        except ValueError:
            print("Opção inválida. Tente novamente.")

def atualizar_cooldowns(cooldowns):
    for habilidade in list(cooldowns):
        cooldowns[habilidade] -= 1
        if cooldowns[habilidade] <= 0:
            del cooldowns[habilidade]