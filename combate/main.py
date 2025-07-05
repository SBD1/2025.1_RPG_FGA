import random
from inteligencia import escolher_acao_monstro
from regras import aplicar_regras
from combate import menu, escolher_habilidade, atualizar_cooldowns
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

habilidades = {
    "ataque": {
        "Chama Sombria": {"tipo": "G", "potencia": 85, "cooldown": 2},
        "Lâmina Fantasma": {"tipo": "P", "potencia": 70, "cooldown": 1},
        "Explosão Arcana": {"tipo": "E", "potencia": 90, "cooldown": 3},
        "Fúria do Trovão": {"tipo": "H", "potencia": 100, "cooldown": 2},
    },
    "defesa": {
        "Barreira de Ferro": {"tipo": "M", "potencia": 60, "cooldown": 2},
        "Escudo de Mana": {"tipo": "G", "potencia": 50, "cooldown": 1},
        "Manto Etéreo": {"tipo": "P", "potencia": 65, "cooldown": 2},
        "Pele de Pedra": {"tipo": "E", "potencia": 75, "cooldown": 3},
    },
    "cura": {
        "Toque Vital": {"tipo": "H", "potencia": 50, "cooldown": 2},
        "Benção da Luz": {"tipo": "M", "potencia": 80, "cooldown": 3},
        "Essência Restauradora": {"tipo": "G", "potencia": 90, "cooldown": 3},
        "Ritual da Vida": {"tipo": "E", "potencia": 100, "cooldown": 4},
    }
}

vida_jogador = 200
vida_monstro = 200
VIDA_MAX = 200
fugiu = False

# Cooldown trackers
cooldowns_jogador = {}
cooldowns_monstro = {}

# Mapeamento do input
categoria_map = {'A': 'ataque', 'D': 'defesa', 'C': 'cura'}

# Loop principal
while vida_jogador > 0 and vida_monstro > 0:
    limpar_tela() 
    menu(vida_jogador, vida_monstro)
    entrada = input("Digite sua escolha: ").upper()

    if entrada == 'F':
        print("🏃 Você fugiu do combate!")
        fugiu = True
        break

    if entrada not in categoria_map:
        print("Opção inválida. Escolha A, D, C ou F.")
        continue

    j_categoria = categoria_map[entrada]
    j_nome, j_habilidade = escolher_habilidade(j_categoria, habilidades, cooldowns_jogador, vida_jogador, vida_monstro)

    if j_nome is None:
        continue  # Se todas as habilidades dessa categoria estiverem em cooldown

    # Escolher ação do monstro com IA adaptativa
    m_categoria, (m_nome, m_habilidade) = escolher_acao_monstro(
        habilidades,
        vida_monstro,
        vida_jogador,
        cooldowns_monstro,
        entrada,
        j_habilidade['tipo']
    )

    # Aplicar efeitos de combate
    vida_jogador, vida_monstro = aplicar_regras(
        j_categoria, j_nome, j_habilidade,
        m_categoria, m_nome, m_habilidade,
        vida_jogador, vida_monstro
    )

    # Aplicar cooldowns após uso
    cooldowns_jogador[j_nome] = j_habilidade.get('cooldown', 0)
    cooldowns_monstro[m_nome] = m_habilidade.get('cooldown', 0)

    # Atualizar cooldowns de turnos anteriores
    atualizar_cooldowns(cooldowns_jogador)
    atualizar_cooldowns(cooldowns_monstro)

# Resultado final
if not fugiu:
    print("\n=========== RESULTADO FINAL ===========")
    if vida_jogador <= 0 and vida_monstro <= 0:
        print("⚔️ Empate! Ambos caíram no campo de batalha!")
    elif vida_jogador <= 0:
        print("💀 Você foi derrotado pelo monstro!")
    elif vida_monstro <= 0:
        print("🏆 Vitória! Você derrotou o monstro!")    
    print("+======================================")
    