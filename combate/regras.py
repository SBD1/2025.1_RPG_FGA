eficacias = {
    'M': {'P': 1.5, 'H': 0.75},
    'P': {'E': 1.5, 'M': 0.75},
    'H': {'M': 1.5, 'G': 0.75},
    'E': {'G': 1.5, 'P': 0.75},
    'G': {'H': 1.5, 'E': 0.75}
}

def eficacia(elemento1, elemento2):
    return eficacias.get(elemento1, {}).get(elemento2, 1)

def mostrar_eficacia(mult, quem=''):
    if mult > 1:
        print(f"🔥 {quem} foi super efetivo! (x{mult:.2f})")
    elif mult < 1:
        print(f"💧 {quem} foi pouco efetivo. (x{mult:.2f})")
    else:
        print(f"🔸 {quem} teve eficácia normal. (x{mult:.2f})")

def aplicar_regras(j_acao, j_nome, j_hab, m_acao, m_nome, m_hab, vida_jogador, vida_monstro):
    j_tipo, j_pot = j_hab['tipo'], j_hab['potencia']
    m_tipo, m_pot = m_hab['tipo'], m_hab['potencia']

    mult_j = eficacia(j_tipo, m_tipo)
    mult_m = eficacia(m_tipo, j_tipo)

    print(f"\n🧙 Jogador usou {j_acao.upper()} - {j_nome} ({j_tipo}) | Potência base: {j_pot}")
    print(f"👹 Monstro usou {m_acao.upper()} - {m_nome} ({m_tipo}) | Potência base: {m_pot}")

    # A X A
    if j_acao == 'ataque' and m_acao == 'ataque':
        dano_j = j_pot * mult_j
        dano_m = m_pot * mult_m
        mostrar_eficacia(mult_j, "Jogador")
        mostrar_eficacia(mult_m, "Monstro")
        print(f"Jogador causou {j_pot:.1f} x {mult_j:.2f} = {dano_j:.1f} de dano")
        print(f"Monstro causou {m_pot:.1f} x {mult_m:.2f} = {dano_m:.1f} de dano")
        vida_monstro -= dano_j
        vida_jogador -= dano_m

    # A X D
    elif j_acao == 'ataque' and m_acao == 'defesa':
        mostrar_eficacia(mult_j, "Jogador")
        mostrar_eficacia(mult_m, "Monstro")
        dano = max(0, (j_pot * mult_j) - (m_pot * mult_m))
        print(f"Jogador causou {j_pot:.1f} x {mult_j:.2f} = {j_pot * mult_j:.1f} de dano base")
        print(f"Monstro defendeu com {m_pot:.1f} x {mult_m:.2f} = {m_pot * mult_m:.1f} de defesa")
        print(f"Dano final sofrido pelo monstro: {dano:.1f}")
        vida_monstro -= dano

    # A X C
    elif j_acao == 'ataque' and m_acao == 'cura':
        mostrar_eficacia(mult_j, "Jogador")
        dano = j_pot * mult_j
        print(f"Jogador causou {j_pot:.1f} x {mult_j:.2f} = {dano:.1f} de dano")
        print(f"💥 Ataque cancelou cura do monstro!")
        vida_monstro -= dano

    # C X C
    elif j_acao == 'cura' and m_acao == 'cura':
        cura_j = j_pot * mult_j
        cura_m = m_pot * mult_m
        mostrar_eficacia(mult_j, "Jogador")
        mostrar_eficacia(mult_m, "Monstro")
        print(f"Jogador curou {j_pot:.1f} x {mult_j:.2f} = {cura_j:.1f}")
        print(f"Monstro curou {m_pot:.1f} x {mult_m:.2f} = {cura_m:.1f}")
        vida_jogador += cura_j
        vida_monstro += cura_m

    # D X D
    elif j_acao == 'defesa' and m_acao == 'defesa':
        print("🧱 Ambos defenderam. Nada aconteceu.")

    # C X D (Jogador cura, monstro defende)
    elif j_acao == 'cura' and m_acao == 'defesa':
        cura = j_pot * mult_j
        mostrar_eficacia(mult_j, "Jogador")
        print(f"Jogador curou {j_pot:.1f} x {mult_j:.2f} = {cura:.1f}")
        print(f"Monstro defendeu à toa.")
        vida_jogador += cura

    # D X C (Jogador defende, monstro cura)
    elif j_acao == 'defesa' and m_acao == 'cura':
        cura = m_pot * mult_m
        mostrar_eficacia(mult_m, "Monstro")
        print(f"Monstro curou {m_pot:.1f} x {mult_m:.2f} = {cura:.1f}")
        print(f"Jogador defendeu à toa.")
        vida_monstro += cura

    # D X A
    elif j_acao == 'defesa' and m_acao == 'ataque':
        mostrar_eficacia(mult_m, "Monstro")
        mostrar_eficacia(mult_j, "Jogador")
        dano = max(0, (m_pot * mult_m) - (j_pot * mult_j))
        print(f"Monstro causou {m_pot:.1f} x {mult_m:.2f} = {m_pot * mult_m:.1f} de dano base")
        print(f"Jogador defendeu com {j_pot:.1f} x {mult_j:.2f} = {j_pot * mult_j:.1f} de defesa")
        print(f"Dano final sofrido pelo jogador: {dano:.1f}")
        vida_jogador -= dano

    # C X A
    elif j_acao == 'cura' and m_acao == 'ataque':
        mostrar_eficacia(mult_m, "Monstro")
        dano = m_pot * mult_m
        print(f"Monstro causou {m_pot:.1f} x {mult_m:.2f} = {dano:.1f} de dano")
        print(f"💥 Monstro cancelou sua cura!")
        vida_jogador -= dano

    # Limitar vida para não ultrapassar máximo ou ficar negativo
    vida_jogador = min(max(vida_jogador, 0), 200)
    vida_monstro = min(max(vida_monstro, 0), 200)

    return vida_jogador, vida_monstro
