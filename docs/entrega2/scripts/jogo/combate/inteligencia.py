# ===== inteligencia.py =====
import random

def escolher_acao_monstro(habilidades, vida_monstro, vida_jogador, cooldowns, ultima_acao_jogador=None, ultimo_tipo_jogador=None):
    vida_max = 100  # Default caso não tenha acesso ao máximo, ajustar no main se precisar
    # Se quiser usar vida max real, passe como parâmetro extra e utilize aqui.

    vida_percentual = vida_monstro / vida_max if vida_max else 1.0

    # Se todas as habilidades estiverem em cooldown, passa o turno
    habilidades_disponiveis = []
    for cat in ['ataque', 'defesa', 'cura']:
        habilidades_categoria = habilidades.get(cat, {})
        disp = [nome for nome in habilidades_categoria if nome not in cooldowns]
        habilidades_disponiveis.extend(disp)

    if not habilidades_disponiveis:
        print(habilidades_disponiveis)
        # Sem habilidade disponível
        return 'passar', (None, None)

    # Escolha de categoria baseada na vida percentual
    if vida_percentual < 0.35:
        categoria = random.choices(['cura', 'defesa', 'ataque'], weights=[0.5, 0.3, 0.2])[0]
    elif vida_jogador < (vida_max * 0.35):
        categoria = random.choices(['ataque', 'defesa', 'cura'], weights=[0.5, 0.3, 0.2])[0]
    else:
        categoria = random.choice(['ataque', 'defesa', 'cura'])

    habilidades_categoria = habilidades.get(categoria, {})
    habilidades_disponiveis = [
        (nome, det) for nome, det in habilidades_categoria.items()
        if nome not in cooldowns
    ]

    if not habilidades_disponiveis:
        # Se categoria sem habilidades disponíveis, tenta outras categorias
        for cat in ['ataque', 'defesa', 'cura']:
            if cat == categoria:
                continue
            habilidades_categoria = habilidades.get(cat, {})
            habilidades_disponiveis = [
                (nome, det) for nome, det in habilidades_categoria.items()
                if nome not in cooldowns
            ]
            if habilidades_disponiveis:
                categoria = cat
                break

    if not habilidades_disponiveis:
        # Mesmo após tentar outras categorias, nada disponível, passa o turno
        return 'passar', (None, None)

    tema_contrario = {
        'M': 'H',
        'P': 'M',
        'H': 'G',
        'E': 'P',
        'G': 'E'
    }

    # Tentar escolher habilidade forte contra o último tipo do jogador
    if ultimo_tipo_jogador:
        fortes_contra_jogador = [
            item for item in habilidades_disponiveis
            if item[1]['tipo'] == tema_contrario.get(ultimo_tipo_jogador)
        ]
        if fortes_contra_jogador:
            return categoria, random.choice(fortes_contra_jogador)

    return categoria, random.choice(habilidades_disponiveis)
