from jogo.db import get_db_connection, clear_screen

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
                xp_max = nivel * 100  # regra provisória
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

def mostrar_menu_afinidade(jogador):
    while True:
        clear_screen()
        print(f"\n=== Afinidades de {jogador['nome']} ===\n")
        afinidades = carregar_afinidades_estudante(jogador['id'])
        if not afinidades:
            print("Nenhuma afinidade encontrada.")
        else:
            # Cabeçalho alinhado
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
        opcao = input("Digite 0 para voltar: ")
        if opcao == '0':
            break
