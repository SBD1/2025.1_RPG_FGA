import random

def escolher_acao_monstro(habilidades, vida_monstro, vida_jogador, cooldowns, ultima_acao_jogador=None, ultimo_tipo_jogador=None):
    # Estratégia básica baseada em estado do combate
    if vida_monstro < 70:
        # Mais propenso a curar se vida baixa
        categoria = random.choices(['cura', 'defesa', 'ataque'], weights=[0.5, 0.3, 0.2])[0]
    elif vida_jogador < 70:
        # Mais propenso a atacar se jogador estiver fraco
        categoria = random.choices(['ataque', 'defesa', 'cura'], weights=[0.5, 0.3, 0.2])[0]
    else:
        categoria = random.choice(['ataque', 'defesa', 'cura'])

    # Priorizar tema forte contra jogador, se possível
    tema_contrario = {
        'M': 'H',
        'P': 'M',
        'H': 'G',
        'E': 'P',
        'G': 'E'
    }

    habilidades_disponiveis = [
        (nome, det) for nome, det in habilidades[categoria].items()
        if nome not in cooldowns
    ]
    if ultimo_tipo_jogador:
        fortes_contra_jogador = [item for item in habilidades_disponiveis if item[1]['tipo'] == tema_contrario.get(ultimo_tipo_jogador)]
        if fortes_contra_jogador:
            return categoria, random.choice(fortes_contra_jogador)

    # Caso contrário, escolha aleatória
    return categoria, random.choice(habilidades_disponiveis)
