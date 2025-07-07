from jogo.db import get_db_connection, clear_screen
from psycopg2 import Error
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Importa as funções de ação
from jogo.map.dungeon import tem_dungeon_interativo
from jogo.map.loja import acessar_loja

# Inicializa o console e a função de verificação de emoji
console = Console()

def _check_emoji_support():
    """Função de verificação de emoji movida para cá para evitar importação circular."""
    import os
    if os.environ.get("WT_SESSION"):
        return True
    if os.environ.get("WSL_DISTRO_NAME"):
        return False
    if os.name != 'nt':
        return True
    return False

EMOJI_SUPPORT = _check_emoji_support()

# --- Funções de Listagem e Movimentação (sem alterações na lógica) ---

def listar_salas(id_estudante=None):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        if id_estudante:
            cur.execute("SELECT id_sala FROM estudante WHERE id_estudante = %s", (id_estudante,))
            sala_atual = cur.fetchone()
            if not sala_atual:
                console.print("Estudante não encontrado ou sem sala atribuída.", style="bold red")
                return []

            sala_atual_id = sala_atual[0]

            query = """
                SELECT s.id_sala, s.nome, s.descricao, c.nome as campus
                FROM sala_comum s
                JOIN setor st ON s.id_setor = st.id_setor
                JOIN campus c ON st.id_campus = c.id_campus
                WHERE s.id_sala IN (
                    SELECT id_prevSala FROM sala_comum WHERE id_sala = %s
                    UNION
                    SELECT id_proxSala FROM sala_comum WHERE id_sala = %s
                )
                ORDER BY s.id_sala
            """
            cur.execute(query, (sala_atual_id, sala_atual_id))
            salas = cur.fetchall()
            
            salas_corrigidas = [(sala[0], sala[1].strip(), sala[2].strip(), sala[3].strip()) for sala in salas]
            return salas_corrigidas

    except (Exception, Error) as e:
        console.print(f"Erro ao listar salas: {e}", style="bold red")
        return []

    finally:
        if conn: conn.close()


def mover_estudante_para_sala(id_estudante, novo_id_sala):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT e.nome, s.nome FROM Estudante e JOIN Sala_Comum s ON e.id_sala = s.id_sala WHERE e.id_estudante = %s", (id_estudante,))
        estudante = cur.fetchone()
        if not estudante:
            console.print("Estudante não encontrado.", style="bold red")
            return False

        cur.execute("SELECT nome FROM Sala_Comum WHERE id_sala = %s", (novo_id_sala,))
        nova_sala = cur.fetchone()
        if not nova_sala:
            console.print("Sala com esse ID não encontrada.", style="bold red")
            return False

        cur.execute("UPDATE Estudante SET id_sala = %s WHERE id_estudante = %s", (novo_id_sala, id_estudante))
        conn.commit()

        console.print(f"Movido de '[cyan]{estudante[1].strip()}[/cyan]' para '[cyan]{nova_sala[0].strip()}[/cyan]' com sucesso!", style="green")
        return True

    except (Exception, Error) as e:
        console.print(f"Erro ao mover estudante: {e}", style="bold red")
        conn.rollback()
        return False

    finally:
        if conn: conn.close()

# --- Funções de Exploração Estilizadas ---

def coletar_itens_da_sala(jogador, itens_no_chao, conn, cur):
    """Lida com a lógica de coletar todos os itens encontrados no chão."""
    clear_screen()
    
    table = Table(title="Itens Encontrados", border_style="yellow")
    table.add_column("Item", style="magenta")
    for _, nome_item in itens_no_chao:
        table.add_row(nome_item.strip())
    console.print(table)

    confirmacao = console.input("\n[bold]Deseja coletar todos os itens? (s/n): [/bold]").strip().lower()
    if confirmacao == 's':
        id_estudante = jogador['id']
        itens_coletados = 0
        for id_instancia, nome_item in itens_no_chao:
            cur.execute(
                "UPDATE instancia_de_item SET id_estudante = %s, id_sala = NULL WHERE id_instanciaItem = %s",
                (id_estudante, id_instancia)
            )
            console.print(f"Você coletou: [yellow]{nome_item.strip()}[/yellow]")
            itens_coletados += 1
        
        if itens_coletados > 0:
            conn.commit()
            console.print("\n[green]Todos os itens foram adicionados ao seu inventário.[/green]")
        else:
            console.print("\n[yellow]Nenhum item foi coletado.[/yellow]")
    else:
        console.print("\nVocê deixou os itens no chão.")
    
    console.input("\n[dim]Pressione Enter para continuar...[/dim]")


def explorar_sala(jogador):
    """Verifica o que há na sala e oferece um menu de ações contextuais estilizado."""
    clear_screen()
    icon_explore = "🔍" if EMOJI_SUPPORT else ""
    console.print(Panel(f"{icon_explore} Explorando [cyan]{jogador['nome_sala'].strip()}[/cyan]...", border_style="blue"))
    id_sala = jogador['id_sala']
    
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT tem_dungeon, tem_loja FROM sala_comum WHERE id_sala = %s", (id_sala,))
        resultado = cur.fetchone()
        tem_dungeon, tem_loja = (False, False) if not resultado else resultado

        cur.execute("""
            SELECT ii.id_instanciaItem, COALESCE(c.nome, e.nome, m.nome) AS nome_item
            FROM instancia_de_item ii
            JOIN tipo_item ti ON ii.id_item = ti.id_item
            LEFT JOIN consumivel c ON ti.id_item = c.id_item
            LEFT JOIN equipavel e ON ti.id_item = e.id_item
            LEFT JOIN monetario m ON ti.id_item = m.id_item
            WHERE ii.id_sala = %s AND ii.id_estudante IS NULL;
        """, (id_sala,))
        itens_no_chao = cur.fetchall()

        opcoes = {}
        contador_opcoes = 1
        
        # Constrói a lista de descobertas
        descobertas_table = Table(show_header=False, show_edge=False, box=None)
        descobertas_table.add_column()
        
        icon_dungeon = "🏰" if EMOJI_SUPPORT else ""
        icon_shop = "🏪" if EMOJI_SUPPORT else ""
        icon_item = "✨" if EMOJI_SUPPORT else ""
        icon_error = "❌" if EMOJI_SUPPORT else "[x]"

        if tem_dungeon:
            descobertas_table.add_row(f"[bold green]{icon_dungeon} Você encontrou a entrada de uma Dungeon![/bold green]")
            opcoes[str(contador_opcoes)] = ("Entrar na Dungeon", lambda: tem_dungeon_interativo(jogador))
            contador_opcoes += 1
        if tem_loja:
            descobertas_table.add_row(f"[bold yellow]{icon_shop} Você encontrou uma Loja![/bold yellow]")
            opcoes[str(contador_opcoes)] = ("Acessar Loja", lambda: acessar_loja(jogador))
            contador_opcoes += 1
        if itens_no_chao:
            descobertas_table.add_row(f"[bold magenta]{icon_item} Você vê alguns itens no chão![/bold magenta]")
            opcoes[str(contador_opcoes)] = ("Coletar Itens", lambda: coletar_itens_da_sala(jogador, itens_no_chao, conn, cur))
            contador_opcoes += 1

        if not opcoes:
            console.print(Panel("[dim]Não há nada de especial por aqui. Apenas o vazio da vida acadêmica.[/dim]", title="Resultado"))
            console.input("\n[dim]Pressione Enter para voltar...[/dim]")
            return
            
        console.print(Panel(descobertas_table, title="[bold]Descobertas[/bold]"))
        
        # Monta a tabela de ações
        acoes_table = Table(show_header=False, show_edge=False, box=None)
        acoes_table.add_column(style="bold cyan", justify="right")
        acoes_table.add_column()
        
        for key, (texto, _) in opcoes.items():
            acoes_table.add_row(f"[{key}]", f" {texto}")
        acoes_table.add_row(f"[{contador_opcoes}]", " Voltar")
        
        console.print(Panel(acoes_table, title="[bold]Ações[/bold]"))

        while True:
            escolha = console.input("\n[bold]O que você deseja fazer? [/bold]").strip()

            if escolha in opcoes:
                texto_acao, acao = opcoes[escolha]
                acao()
                break 
            elif escolha == str(contador_opcoes):
                console.print("Voltando ao menu...", style="yellow")
                break
            else:
                clear_screen()
                console.print(Panel(f"{icon_explore} Explorando [cyan]{jogador['nome_sala'].strip()}[/cyan]...", border_style="blue"))
                console.print(Panel(descobertas_table, title="[bold]Descobertas[/bold]"))
                console.print(Panel(acoes_table, title="[bold]Ações[/bold]"))
                console.print(f"\n{icon_error} [bold red]Opção inválida. Tente novamente.[/bold red]")


    except (Exception, Error) as e:
        if conn: conn.rollback()
        icon_error_fatal = "❌" if EMOJI_SUPPORT else "[x]"
        console.print(f"{icon_error_fatal} Erro ao explorar a sala: {e}", style="bold red")
    finally:
        if conn: conn.close()
