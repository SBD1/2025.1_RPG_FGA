import random
from inteligencia import escolher_acao_monstro
from regras import aplicar_regras
from combate import menu, escolher_habilidade

# Habilidades definidas aqui para manter centralizado
habilidades = {
    "ataque": {
        "Chama Sombria": {"tipo": "G", "potencia": 85},
        "Lâmina Fantasma": {"tipo": "P", "potencia": 70},
        "Explosão Arcana": {"tipo": "E", "potencia": 90},
        "Fúria do Trovão": {"tipo": "H", "potencia": 100},
    },
    "defesa": {
        "Barreira de Ferro": {"tipo": "M", "potencia": 60},
        "Escudo de Mana": {"tipo": "G", "potencia": 50},
        "Manto Etéreo": {"tipo": "P", "potencia": 65},
        "Pele de Pedra": {"tipo": "E", "potencia": 75},
    },
    "cura": {
        "Toque Vital": {"tipo": "H", "potencia": 50},
        "Benção da Luz": {"tipo": "M", "potencia": 80},
        "Essência Restauradora": {"tipo": "G", "potencia": 90},
        "Ritual da Vida": {"tipo": "E", "potencia": 100},
    }
}

vida_jogador = 200
vida_monstro = 200
VIDA_MAX = 200
fugiu = False

categoria_map = {'A': 'ataque', 'D': 'defesa', 'C': 'cura'}

while vida_jogador > 0 and vida_monstro > 0:
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
    j_nome, j_habilidade = escolher_habilidade(j_categoria, habilidades)

    m_categoria, (m_nome, m_habilidade) = escolher_acao_monstro(habilidades)

    vida_jogador, vida_monstro = aplicar_regras(
        j_categoria, j_nome, j_habilidade,
        m_categoria, m_nome, m_habilidade,
        vida_jogador, vida_monstro
    )

if not fugiu:
    print("\n=========== RESULTADO FINAL ===========")
    if vida_jogador <= 0 and vida_monstro <= 0:
        print("⚔️ Empate! Ambos caíram no campo de batalha!")
    elif vida_jogador <= 0:
        print("💀 Você foi derrotado pelo monstro!")
    elif vida_monstro <= 0:
        print("🏆 Vitória! Você derrotou o monstro!")
