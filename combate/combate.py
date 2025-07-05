import os
import sys

def limpar_tela():
    try:
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
    except:
        
        print('\n' * 100)

    if sys.stdout.isatty():
        print("\033[H\033[J", end='')  

def barra_vida(vida, nome):
    blocos = int(vida // 20)
    vazios = 10 - blocos
    barra = "🟥" * blocos + "⬛" * vazios
    print(f"{nome}: [{barra}] {vida:.0f}/200")

def menu(vida_jogador, vida_monstro):
    print('\n============== HORA DO DUELO ==============')
    barra_vida(vida_jogador, "🧙 Jogador")
    barra_vida(vida_monstro, "👹 Monstro")
    print('Escolha o que deseja realizar:')
    print('[A] Habilidade de Ataque')
    print('[D] Habilidade de Defesa')
    print('[C] Habilidade de Cura')
    print('[F] Fugir')
    print('===========================================')

def lista_habilidades(categoria_dict):
    tipo_emojis = {
        "M": "📐", "P": "💻", "E": "⚙️", "H": "📚", "G": "🌐"
    }
    tipo_nome = {
        "M": "Matemática", "P": "Programação", "E": "Engenharias",
        "H": "Humanidades", "G": "Gerais"
    }

    
    for i, (nome, detalhes) in enumerate(categoria_dict.items(), 1):
        tipo = detalhes["tipo"]
        potencia = detalhes["potencia"]
        print(f"[{i}] {nome:<25} | Potência: {potencia:<3} | Tema: {tipo_emojis[tipo]} {tipo_nome[tipo]:<12} ")
    
def escolher_habilidade(categoria, habilidades, cooldowns, vida_jogador, vida_monstro):
    limpar_tela()
    habilidades_categoria = {
        nome: det for nome, det in habilidades[categoria].items()
        if nome not in cooldowns
    }

    if not habilidades_categoria:
        print("⏳ Todas as habilidades dessa categoria estão em cooldown. Escolha outra ação.")
        return None, None

    habilidades_nomes = {
        "ataque": "HABILIDADES DE ATAQUE ",
        "defesa": "HABILIDADES DE DEFESA ",
        "cura": "HABILIDADES DE CURA "
    }
    
    print('\n======================'+ f" MENU DE {habilidades_nomes.get(categoria, 'HABILIDADES')}"+ '======================')

    
    lista_habilidades(habilidades_categoria)
    print("\n📊 Vida atual:")
    print(f"🧙 Jogador: {vida_jogador:.0f}/200")
    print(f"👹 Monstro: {vida_monstro:.0f}/200")


    print('===========================================================================')

    while True:
        try:
            escolha = int(input("Escolha a habilidade [1-4]: ")) - 1
            habilidades_lista = list(habilidades_categoria.items())
            if 0 <= escolha < len(habilidades_lista):
                return habilidades_lista[escolha]
        except ValueError:
            pass
        print("Opção inválida. Tente novamente.")
    
        
def atualizar_cooldowns(cooldowns):
    for habilidade in list(cooldowns):
        cooldowns[habilidade] -= 1
        if cooldowns[habilidade] <= 0:
            del cooldowns[habilidade]
