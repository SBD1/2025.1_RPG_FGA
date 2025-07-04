import random

def escolher_acao_monstro(habilidades):
    categoria = random.choice(['ataque', 'defesa', 'cura'])
    habilidade = random.choice(list(habilidades[categoria].items()))
    return categoria, habilidade
