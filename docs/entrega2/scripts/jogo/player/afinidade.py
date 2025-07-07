from jogo.db import get_db_connection, clear_screen
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
# A importação problemática foi removida do topo do arquivo

# Inicializa o console da Rich
console = Console()

EMOJIS_TEMA_ID = {
    1: '📐', 2: '💻', 3: '⚙️', 4: '📚', 5: '🌐',
}

def barra_progresso(valor_atual, valor_maximo, tamanho=10):
    """Cria uma barra de progresso com emojis ou caracteres de fallback."""
    # A importação é feita aqui para evitar o ciclo
    from .menu import check_emoji_support
    EMOJI_SUPPORT = check_emoji_support()
    
    proporcao = valor_atual / valor_maximo if valor_maximo > 0 else 0
    blocos_cheios = int(proporcao * tamanho)
    blocos_vazios = tamanho - blocos_cheios
    
    bar = Text()
    if EMOJI_SUPPORT:
        bar.append("🟩" * blocos_cheios)
        bar.append("⬛" * blocos_vazios)
    else:
        bar.append("*" * blocos_cheios, style="bold green")
        bar.append("-" * blocos_vazios, style="white")
    return bar

def verificar_level_up(id_estudante, id_tema):
    """Verifica e aplica o level up para uma afinidade específica."""
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT xp_atual, nivel_atual FROM afinidade WHERE id_estudante = %s AND id_tema = %s FOR UPDATE", (id_estudante, id_tema))
            res = cur.fetchone()
            if not res: return

            xp_atual, nivel = res
            mudou = False
            xp_max = lambda n: round(50 * (n ** 1.5))

            while xp_atual >= xp_max(nivel) and nivel < 20:
                xp_atual -= xp_max(nivel)
                nivel += 1
                mudou = True
            
            if nivel >= 20: xp_atual = xp_max(20)

            if mudou:
                cur.execute("UPDATE afinidade SET xp_atual = %s, nivel_atual = %s WHERE id_estudante = %s AND id_tema = %s", (xp_atual, nivel, id_estudante, id_tema))
                conn.commit()
    except Exception as e:
        console.print(f"[bold red]Erro ao verificar level up: {e}[/bold red]")
    finally:
        if conn: conn.close()

def carregar_afinidades_estudante(id_estudante):
    """Carrega as afinidades de um estudante do banco de dados."""
    query = "SELECT a.id_tema, t.nome, a.nivel_atual, a.xp_atual FROM afinidade a JOIN tema t ON a.id_tema = t.id_tema WHERE a.id_estudante = %s ORDER BY a.id_tema;"
    afinidades = []
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute(query, (id_estudante,))
            rows = cur.fetchall()
            for row in rows:
                id_tema, nome_tema, nivel, xp_atual = row
                verificar_level_up(id_estudante, id_tema)
                
                cur.execute("SELECT nivel_atual, xp_atual FROM afinidade WHERE id_estudante = %s AND id_tema = %s", (id_estudante, id_tema))
                nivel, xp_atual = cur.fetchone()
                xp_max = round(50 * (nivel ** 1.5))

                afinidades.append({'id_tema': id_tema, 'nome_tema': nome_tema.strip(), 'nivel': nivel, 'xp_atual': xp_atual, 'xp_max': xp_max})
    except Exception as e:
        console.print(f"[bold red]Erro ao carregar afinidades: {e}[/bold red]")
    finally:
        if conn: conn.close()
    return afinidades

# ======== FUNÇÃO ATUALIZADA ========
def mostrar_menu_afinidade(jogador):
    """Exibe as afinidades do jogador e espera o usuário pressionar Enter para voltar."""
    # A importação é feita aqui para evitar o ciclo
    from .menu import check_emoji_support
    EMOJI_SUPPORT = check_emoji_support()
    
    clear_screen()
    afinidades = carregar_afinidades_estudante(jogador['id'])
    
    table = Table(title=f"Afinidades de {jogador['nome']}", border_style="blue")
    table.add_column("Tema", style="magenta", width=20)
    table.add_column("Nível", style="cyan", justify="center")
    table.add_column("Progresso de XP", style="green")

    if not afinidades:
        console.print(Panel("[yellow]Nenhuma afinidade encontrada.[/yellow]", title="Aviso"))
    else:
        for a in afinidades:
            emoji = EMOJIS_TEMA_ID.get(a['id_tema'], '❓') if EMOJI_SUPPORT else ""
            
            # Verifica se o nível é máximo para exibir a mensagem correta
            if a['nivel'] == 20:
                # Usa a verificação de suporte para o emoji de brilho
                max_text = "✨ Maximizado! ✨" if EMOJI_SUPPORT else "Maximizado!"
                xp_formatado = Text(max_text, style="bold yellow")
            else:
                barra = barra_progresso(a['xp_atual'], a['xp_max'])
                xp_formatado = Text.assemble(f"[{barra}] ", (f"{a['xp_atual']}/{a['xp_max']}", "bold white"))
            
            table.add_row(f"{emoji} {a['nome_tema']}", str(a['nivel']), xp_formatado)
        console.print(table)
