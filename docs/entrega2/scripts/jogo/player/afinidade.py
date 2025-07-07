from jogo.db import get_db_connection, clear_screen
import statistics


EMOJIS_TEMA_ID = {
    1: '📐',  # Matemática
    2: '💻',  # Programação
    3: '⚙️',  # Engenharias
    4: '📚',  # Humanidades
    5: '🌐',  # Gerais
}

def barra_progresso(valor_atual, valor_maximo, tamanho=10):
    proporcao = valor_atual / valor_maximo if valor_maximo > 0 else 0
    blocos_cheios = int(proporcao * tamanho)
    blocos_vazios = tamanho - blocos_cheios
    return '🟩' * blocos_cheios + '⬛' * blocos_vazios

def verificar_level_up(id_estudante, id_tema):
    """
    Verifica se o XP atual ultrapassa o XP necessário para o level up.
    Caso sim, desconta o XP necessário e incrementa o nível,
    repete até não ser mais possível upar.
    Usa fórmula mais justa para XP máximo: 50 * nível^1.5 arredondado.
    """
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            # Busca xp e nivel atuais
            cur.execute("""
                SELECT xp_atual, nivel_atual
                FROM afinidade
                WHERE id_estudante = %s AND id_tema = %s
                FOR UPDATE
            """, (id_estudante, id_tema))
            res = cur.fetchone()
            if not res:
                return  # Nada a fazer se não existe afinidade

            xp_atual, nivel = res
            mudou = False

            # Função para calcular xp max (fórmula justa)
            def xp_max(n):
                return round(50 * (n ** 1.5))

            while xp_atual >= xp_max(nivel):
                xp_atual -= xp_max(nivel)
                nivel += 1
                mudou = True
                if nivel > 20:  # limite maximo de nível
                    nivel = 20
                    xp_atual = xp_max(nivel)
                    break

            if mudou:
                cur.execute("""
                    UPDATE afinidade
                    SET xp_atual = %s, nivel_atual = %s
                    WHERE id_estudante = %s AND id_tema = %s
                """, (xp_atual, nivel, id_estudante, id_tema))
                conn.commit()

    except Exception as e:
        print(f"Erro ao verificar level up: {e}")
    finally:
        if conn:
            conn.close()

def carregar_afinidades_estudante(id_estudante):
    query = """
        SELECT a.id_tema, t.nome AS nome_tema, a.nivel_atual, a.xp_atual
        FROM afinidade a
        JOIN tema t ON a.id_tema = t.id_tema
        WHERE a.id_estudante = %s
        ORDER BY a.id_tema;
    """
    conn = None
    afinidades = []
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute(query, (id_estudante,))
            rows = cur.fetchall()
            for row in rows:
                id_tema = row[0]
                nome_tema = row[1]
                nivel = row[2]
                xp_atual = row[3]
                # Calcula XP max pela fórmula justa
                xp_max = round(50 * (nivel ** 1.5))
                # Verifica level up automático (sincroniza com o banco)
                verificar_level_up(id_estudante, id_tema)

                # Após level up, recarrega os valores atualizados:
                cur.execute("""
                    SELECT nivel_atual, xp_atual FROM afinidade
                    WHERE id_estudante = %s AND id_tema = %s
                """, (id_estudante, id_tema))
                nivel, xp_atual = cur.fetchone()
                xp_max = round(50 * (nivel ** 1.5))

                afinidades.append({
                    'id_tema': id_tema,
                    'nome_tema': nome_tema,
                    'nivel': nivel,
                    'xp_atual': xp_atual,
                    'xp_max': xp_max
                })
    except Exception as e:
        print(f"Erro ao carregar afinidades: {e}")
    finally:
        if conn:
            conn.close()
    return afinidades

def cheat_menu(id_estudante):
    """
    Menu cheat para alterar nível da afinidade manualmente (nível 1 a 20), resetando XP.
    """
    afinidades = carregar_afinidades_estudante(id_estudante)
    if not afinidades:
        print("Nenhuma afinidade para alterar.")
        input("Pressione Enter para continuar...")
        return

    print("\n=== Cheat Menu: Alterar Nível de Afinidade ===")
    for idx, a in enumerate(afinidades, 1):
        emoji = EMOJIS_TEMA_ID.get(a['id_tema'], '❓')
        print(f"[{idx}] {emoji} {a['nome_tema']} (Nível atual: {a['nivel']})")
    print("[0] Cancelar")

    escolha = input("Escolha a afinidade para alterar o nível: ").strip()
    if not escolha.isdigit():
        print("Entrada inválida.")
        input("Pressione Enter para continuar...")
        return

    escolha = int(escolha)
    if escolha == 0:
        return
    if escolha < 1 or escolha > len(afinidades):
        print("Opção inválida.")
        input("Pressione Enter para continuar...")
        return

    afinidade_selecionada = afinidades[escolha - 1]

    nivel_novo = input("Digite o novo nível (1 a 20): ").strip()
    if not nivel_novo.isdigit():
        print("Nível inválido.")
        input("Pressione Enter para continuar...")
        return

    nivel_novo = int(nivel_novo)
    if nivel_novo < 1 or nivel_novo > 20:
        print("Nível fora do intervalo permitido.")
        input("Pressione Enter para continuar...")
        return

    # Atualiza no banco: nivel novo, xp zero
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE afinidade
                SET nivel_atual = %s, xp_atual = 0
                WHERE id_estudante = %s AND id_tema = %s
            """, (nivel_novo, id_estudante, afinidade_selecionada['id_tema']))
            conn.commit()
        print(f"Nível da afinidade '{afinidade_selecionada['nome_tema']}' atualizado para {nivel_novo} e XP zerado.")
    except Exception as e:
        print(f"Erro ao atualizar nível: {e}")
    finally:
        if conn:
            conn.close()

    input("Pressione Enter para continuar...")

def mostrar_menu_afinidade(jogador):
    while True:
        clear_screen()
        print(f"\n=== Afinidades de {jogador['nome']} ===\n")
        afinidades = carregar_afinidades_estudante(jogador['id'])
        if not afinidades:
            print("Nenhuma afinidade encontrada.")
        else:
            print(f"{'Tema':<18} {'Nível':>5}  {'XP':<15}")
            print("-" * 40)
            for a in afinidades:
                emoji = EMOJIS_TEMA_ID.get(a['id_tema'], '❓')
                barra = barra_progresso(a['xp_atual'], a['xp_max'])
                tema_formatado = f"{emoji} {a['nome_tema']}"
                nivel_formatado = f"{a['nivel']:>5}"
                xp_formatado = f"[{barra}] {a['xp_atual']}/{a['xp_max']}"
                print(f"{tema_formatado:<18} {nivel_formatado}  {xp_formatado:<15}")
        print("\n[0] Voltar")
        print("[9] Cheat Menu (Alterar Nível)")
        opcao = input("Escolha uma opção: ").strip()
        if opcao == '0':
            break
        elif opcao == '9':
            cheat_menu(jogador['id'])


def calcular_vida_maxima_por_afinidades(conn, id_estudante):
    """
    Carrega níveis das afinidades, atualiza níveis com level up se necessário,
    e calcula a vida máxima do jogador.
    """
    niveis = []
    try:
        with conn.cursor() as cur:
            # Primeiro busca os ids de temas do jogador para verificar level up
            cur.execute("""
                SELECT id_tema
                FROM afinidade
                WHERE id_estudante = %s
                ORDER BY id_tema
            """, (id_estudante,))
            temas = [row[0] for row in cur.fetchall()]

        # Para cada tema, verificar e atualizar level up
        for tema_id in temas:
            verificar_level_up(id_estudante, tema_id)

        # Depois de atualizar níveis, buscar os níveis atualizados
        with conn.cursor() as cur:
            cur.execute("""
                SELECT nivel_atual
                FROM afinidade
                WHERE id_estudante = %s
                ORDER BY id_tema
            """, (id_estudante,))
            niveis = [row[0] for row in cur.fetchall()]

    except Exception as e:
        print(f"Erro ao carregar níveis para vida: {e}")
        return 20  # valor base

    if not niveis or len(niveis) < 5:
        return 20  # valor base caso falte info

    VIDA_BASE = 20
    soma_niveis = sum(niveis)
    desvio = statistics.stdev(niveis) if len(set(niveis)) > 1 else 0
    multiplicador = max(0, 4.8 - desvio * 0.25)
    vida_maxima = VIDA_BASE + int(soma_niveis * multiplicador)

    return vida_maxima