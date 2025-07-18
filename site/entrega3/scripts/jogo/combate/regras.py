# ===== regras.py =====

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

def aplicar_regras(j_acao, j_nome, j_hab, m_acao, m_nome, m_hab, vida_jogador, vida_monstro, vida_max_jogador, vida_max_monstro):
    print('\n====================== BATALHA EM ANDAMENTO ======================')

    # Quando jogador ou monstro passam o turno:
    if j_acao == 'passar' and m_acao == 'passar':
        print("Ambos passaram o turno. Nada aconteceu.")
    elif j_acao == 'passar':
        print(f"🧙 Jogador passou o turno.")
    elif m_acao == 'passar':
        print(f"👹 Monstro passou o turno.")

    # Se ambos passaram, nenhuma ação a aplicar:
    if j_acao == 'passar' and m_acao == 'passar':
        print("\n📊 Vida atual:")
        print(f"🧙 Jogador: {vida_jogador:.0f}/{vida_max_jogador}")
        print(f"👹 Monstro: {vida_monstro:.0f}/{vida_max_monstro}")
        print('==================================================================')
        input("\nPressione ENTER para continuar...")
        return vida_jogador, vida_monstro

    # Se jogador passou, monstro age normalmente
    if j_acao == 'passar' and m_acao != 'passar':
        m_tipo, m_pot = m_hab['tipo'], m_hab['potencia']
        mult_m = eficacia(m_tipo, 'G')  # usar eficácia genérica contra jogador que passou (sem tema)
        print(f"👹 Monstro usou: {m_acao.upper():<7} → ✨ {m_nome} | Tema: {m_tipo} | Potência: {m_pot}")
        mostrar_eficacia(mult_m, "Monstro")
        if m_acao == 'ataque':
            print(f"💥 Monstro causou: {m_pot:.1f} de dano")
            vida_jogador -= m_pot
        elif m_acao == 'cura':
            cura = m_pot
            print(f"💖 Monstro curou: {cura:.1f} pontos")
            vida_monstro += cura
        elif m_acao == 'defesa':
            print("🛡️ Monstro defendeu. Nada aconteceu com ele.")
        else:
            print("Ação do monstro não reconhecida.")

    # Se monstro passou, jogador age normalmente
    elif m_acao == 'passar' and j_acao != 'passar':
        j_tipo, j_pot = j_hab['tipo'], j_hab['potencia']
        mult_j = eficacia(j_tipo, 'G')  # eficácia genérica contra monstro que passou
        print(f"🧙 Jogador usou:  {j_acao.upper():<7} → ✨ {j_nome} | Tema: {j_tipo} | Potência: {j_pot}")
        mostrar_eficacia(mult_j, "Jogador")
        if j_acao == 'ataque':
            print(f"💥 Jogador causou: {j_pot:.1f} de dano")
            vida_monstro -= j_pot
        elif j_acao == 'cura':
            cura = j_pot
            print(f"💖 Jogador curou: {cura:.1f} pontos")
            vida_jogador += cura
        elif j_acao == 'defesa':
            print("🛡️ Jogador defendeu. Nada aconteceu com ele.")
        else:
            print("Ação do jogador não reconhecida.")

    # Se ambos agiram (não passaram), aplicar regras normais
    else:
        j_tipo, j_pot = j_hab['tipo'], j_hab['potencia']
        m_tipo, m_pot = m_hab['tipo'], m_hab['potencia']

        mult_j = eficacia(j_tipo, m_tipo)
        mult_m = eficacia(m_tipo, j_tipo)

        print(f"🧙 Jogador usou:  {j_acao.upper():<7} → ✨ {j_nome} | Tema: {j_tipo} | Potência: {j_pot}")
        print(f"👹 Monstro usou: {m_acao.upper():<7} → ✨ {m_nome} | Tema: {m_tipo} | Potência: {m_pot}\n")

        # A X A
        if j_acao == 'ataque' and m_acao == 'ataque':
            dano_j = j_pot * mult_j
            dano_m = m_pot * mult_m
            mostrar_eficacia(mult_j, "Jogador")
            mostrar_eficacia(mult_m, "Monstro")
            print(f"💥 Jogador causou: {dano_j:.1f} de dano")
            print(f"💥 Monstro causou: {dano_m:.1f} de dano")
            vida_monstro -= dano_j
            vida_jogador -= dano_m

        # A X D
        elif j_acao == 'ataque' and m_acao == 'defesa':
            mostrar_eficacia(mult_j, "Jogador")
            mostrar_eficacia(mult_m, "Monstro")
            dano = max(0, (j_pot * mult_j) - (m_pot * mult_m))
            print(f"💥 Dano do jogador: {j_pot:.1f} × {mult_j:.2f} = {j_pot * mult_j:.1f}")
            print(f"🛡️ Defesa do monstro: {m_pot:.1f} × {mult_m:.2f} = {m_pot * mult_m:.1f}")
            print(f"🎯 Dano final sofrido pelo monstro: {dano:.1f}")
            vida_monstro -= dano

        # A X C
        elif j_acao == 'ataque' and m_acao == 'cura':
            mostrar_eficacia(mult_j, "Jogador")
            dano = j_pot * mult_j
            print(f"💥 Jogador causou: {dano:.1f} de dano")
            print(f"💔 Ataque cancelou a cura do monstro!")
            vida_monstro -= dano

        # C X C
        elif j_acao == 'cura' and m_acao == 'cura':
            cura_j = j_pot * mult_j
            cura_m = m_pot * mult_m
            mostrar_eficacia(mult_j, "Jogador")
            mostrar_eficacia(mult_m, "Monstro")
            print(f"💖 Jogador curou:  {cura_j:.1f} pontos")
            print(f"💖 Monstro curou:   {cura_m:.1f} pontos")
            vida_jogador += cura_j
            vida_monstro += cura_m

        # D X D
        elif j_acao == 'defesa' and m_acao == 'defesa':
            print("🧱 Ambos defenderam. Nada aconteceu.")

        # C X D
        elif j_acao == 'cura' and m_acao == 'defesa':
            cura = j_pot * mult_j
            mostrar_eficacia(mult_j, "Jogador")
            print(f"💖 Jogador curou:  {cura:.1f} pontos")
            print(f"🛡️ Monstro defendeu à toa.")
            vida_jogador += cura

        # D X C
        elif j_acao == 'defesa' and m_acao == 'cura':
            cura = m_pot * mult_m
            mostrar_eficacia(mult_m, "Monstro")
            print(f"💖 Monstro curou:  {cura:.1f} pontos")
            print(f"🛡️ Jogador defendeu à toa.")
            vida_monstro += cura

        # D X A
        elif j_acao == 'defesa' and m_acao == 'ataque':
            mostrar_eficacia(mult_m, "Monstro")
            mostrar_eficacia(mult_j, "Jogador")
            dano = max(0, (m_pot * mult_m) - (j_pot * mult_j))
            print(f"💥 Monstro causou: {m_pot * mult_m:.1f} de dano base")
            print(f"🛡️ Jogador defendeu com: {j_pot * mult_j:.1f}")
            print(f"🎯 Dano final sofrido pelo jogador: {dano:.1f}")
            vida_jogador -= dano

        # C X A
        elif j_acao == 'cura' and m_acao == 'ataque':
            mostrar_eficacia(mult_m, "Monstro")
            dano = m_pot * mult_m
            print(f"💥 Monstro causou: {dano:.1f} de dano")
            print(f"💔 Monstro cancelou sua cura!")
            vida_jogador -= dano

        else:
            print("Ações não reconhecidas. Nada aconteceu.")

    # Garantir limites de vida dinâmicos
    vida_jogador = min(max(vida_jogador, 0), vida_max_jogador)
    vida_monstro = min(max(vida_monstro, 0), vida_max_monstro)

    print("\n📊 Vida atual:")
    print(f"🧙 Jogador: {vida_jogador:.0f}/{vida_max_jogador}")
    print(f"👹 Monstro: {vida_monstro:.0f}/{vida_max_monstro}")
    print('==================================================================')
    input("\nPressione ENTER para continuar...")

    return vida_jogador, vida_monstro
