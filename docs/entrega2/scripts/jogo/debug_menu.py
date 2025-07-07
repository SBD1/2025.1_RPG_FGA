# jogo/debug_menu.py

from .db import get_db_connection, clear_screen
from psycopg2 import Error
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from .player.menu import check_emoji_support # Reutiliza a função de verificação

# Inicializa o console e verifica o suporte a emojis
console = Console()
EMOJI_SUPPORT = check_emoji_support()

def listar_salas_com_dungeon():
    """Consulta e exibe todas as salas com dungeon em uma tabela Rich."""
    clear_screen()
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT s.id_sala, s.nome, st.nome AS nome_setor
            FROM sala_comum s
            JOIN setor st ON s.id_setor = st.id_setor
            WHERE s.tem_dungeon = TRUE ORDER BY s.id_sala;
        """)
        salas = cur.fetchall()

        title = "🏰 Salas com Dungeon" if EMOJI_SUPPORT else "Salas com Dungeon"
        table = Table(title=title, border_style="cyan")
        table.add_column("ID Sala", style="magenta")
        table.add_column("Nome da Sala", style="green")
        table.add_column("Setor", style="yellow")

        if not salas:
            console.print(Panel("[yellow]Nenhuma sala com dungeon encontrada.[/yellow]", title="Resultado"))
        else:
            for sala in salas:
                table.add_row(str(sala[0]), sala[1].strip(), sala[2].strip())
            console.print(table)
        
        cur.close()
        conn.close()
    except (Exception, Error) as e:
        console.print(f"[bold red]Erro ao buscar salas com dungeon: {e}[/bold red]")

    console.input("\n[dim]Pressione Enter para voltar...[/dim]")

def listar_salas_com_loja():
    """Consulta e exibe todas as salas com loja em uma tabela Rich."""
    clear_screen()
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT s.id_sala, s.nome, st.nome AS nome_setor
            FROM sala_comum s
            JOIN setor st ON s.id_setor = st.id_setor
            WHERE s.tem_loja = TRUE ORDER BY s.id_sala;
        """)
        salas = cur.fetchall()

        title = "🏪 Salas com Loja" if EMOJI_SUPPORT else "Salas com Loja"
        table = Table(title=title, border_style="cyan")
        table.add_column("ID Sala", style="magenta")
        table.add_column("Nome da Sala", style="green")
        table.add_column("Setor", style="yellow")

        if not salas:
            console.print(Panel("[yellow]Nenhuma sala com loja encontrada.[/yellow]", title="Resultado"))
        else:
            for sala in salas:
                table.add_row(str(sala[0]), sala[1].strip(), sala[2].strip())
            console.print(table)

        cur.close()
        conn.close()
    except (Exception, Error) as e:
        console.print(f"[bold red]Erro ao buscar salas com loja: {e}[/bold red]")

    console.input("\n[dim]Pressione Enter para voltar...[/dim]")

def listar_salas_com_itens():
    """Consulta e exibe todas as salas com itens no chão em uma tabela Rich."""
    clear_screen()
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT s.id_sala, s.nome, COUNT(ii.id_instanciaItem) AS quantidade_itens
            FROM sala_comum s
            JOIN instancia_de_item ii ON s.id_sala = ii.id_sala
            WHERE ii.id_estudante IS NULL
            GROUP BY s.id_sala, s.nome ORDER BY s.id_sala;
        """)
        salas = cur.fetchall()

        title = "✨ Salas com Itens no Chão" if EMOJI_SUPPORT else "Salas com Itens no Chão"
        table = Table(title=title, border_style="cyan")
        table.add_column("ID Sala", style="magenta")
        table.add_column("Nome da Sala", style="green")
        table.add_column("Qtd. de Itens", style="yellow")

        if not salas:
            console.print(Panel("[yellow]Nenhuma sala com itens no chão encontrada.[/yellow]", title="Resultado"))
        else:
            for sala in salas:
                table.add_row(str(sala[0]), sala[1].strip(), str(sala[2]))
            console.print(table)

        cur.close()
        conn.close()
    except (Exception, Error) as e:
        console.print(f"[bold red]Erro ao buscar salas com itens: {e}[/bold red]")

    console.input("\n[dim]Pressione Enter para voltar...[/dim]")

def listar_posicao_jogadores():
    """Consulta e exibe a localização de todos os jogadores em uma tabela Rich."""
    clear_screen()
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT e.nome, s.nome, st.nome
            FROM estudante e
            JOIN sala_comum s ON e.id_sala = s.id_sala
            JOIN setor st ON s.id_setor = st.id_setor
            ORDER BY e.id_estudante;
        """)
        jogadores = cur.fetchall()

        title = "📍 Posição dos Jogadores" if EMOJI_SUPPORT else "Posição dos Jogadores"
        table = Table(title=title, border_style="cyan")
        table.add_column("Jogador", style="magenta")
        table.add_column("Sala Atual", style="green")
        table.add_column("Setor", style="yellow")

        if not jogadores:
            console.print(Panel("[yellow]Nenhum jogador encontrado.[/yellow]", title="Resultado"))
        else:
            for jogador in jogadores:
                table.add_row(jogador[0].strip(), jogador[1].strip(), jogador[2].strip())
            console.print(table)

        cur.close()
        conn.close()
    except (Exception, Error) as e:
        console.print(f"[bold red]Erro ao buscar a posição dos jogadores: {e}[/bold red]")

    console.input("\n[dim]Pressione Enter para voltar...[/dim]")

def listar_detalhes_dungeons():
    """Consulta e exibe informações detalhadas de todas as dungeons em uma tabela Rich."""
    clear_screen()
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT s.id_sala, s.nome, d.nome, t.nome
            FROM sala_comum s
            JOIN dungeon_academica d ON d.id_dungeon = s.id_sala
            JOIN tema t ON d.id_tema = t.id_tema
            ORDER BY s.id_sala;
        """)
        dungeons = cur.fetchall()

        title = "📜 Detalhes das Dungeons" if EMOJI_SUPPORT else "Detalhes das Dungeons"
        table = Table(title=title, border_style="cyan")
        table.add_column("ID Sala", style="magenta")
        table.add_column("Nome da Sala", style="green")
        table.add_column("Nome da Dungeon", style="yellow")
        table.add_column("Tema", style="blue")

        if not dungeons:
            console.print(Panel("[yellow]Nenhuma dungeon encontrada.[/yellow]", title="Resultado"))
        else:
            for dungeon in dungeons:
                table.add_row(str(dungeon[0]), dungeon[1].strip(), dungeon[2].strip(), dungeon[3].strip())
            console.print(table)

        cur.close()
        conn.close()
    except (Exception, Error) as e:
        console.print(f"[bold red]Erro ao buscar detalhes das dungeons: {e}[/bold red]")

    console.input("\n[dim]Pressione Enter para voltar...[/dim]")


def menu_debug_queries():
    """Exibe o menu de consultas de debug estilizado com Rich."""
    icon_dungeon = "🏰" if EMOJI_SUPPORT else ""
    icon_shop = "🏪" if EMOJI_SUPPORT else ""
    icon_item = "✨" if EMOJI_SUPPORT else ""
    icon_player = "📍" if EMOJI_SUPPORT else ""
    icon_details = "📜" if EMOJI_SUPPORT else ""
    icon_back = "↩️" if EMOJI_SUPPORT else ""

    while True:
        clear_screen()
        
        menu_table = Table(show_header=False, show_edge=False, box=None)
        menu_table.add_column(style="bold magenta", justify="right")
        menu_table.add_column(justify="left")

        menu_table.add_row("[1]", f" {icon_dungeon} Listar salas com Dungeon")
        menu_table.add_row("[2]", f" {icon_shop} Listar salas com Loja")
        menu_table.add_row("[3]", f" {icon_item} Listar salas com Itens no Chão")
        menu_table.add_row("[4]", f" {icon_player} Mostrar Posição dos Jogadores")
        menu_table.add_row("[5]", f" {icon_details} Ver Detalhes das Dungeons")
        menu_table.add_row("[6]", f" {icon_back} Voltar ao Menu Principal")
        
        console.print(Panel(menu_table, title="[bold cyan]Menu de Debug[/bold cyan]", border_style="blue"))
        
        opcao = console.input("[bold]Escolha uma opção: [/bold]").strip()

        if opcao == '1':
            listar_salas_com_dungeon()
        elif opcao == '2':
            listar_salas_com_loja()
        elif opcao == '3':
            listar_salas_com_itens()
        elif opcao == '4':
            listar_posicao_jogadores()
        elif opcao == '5':
            listar_detalhes_dungeons()
        elif opcao == '6':
            console.print("Retornando ao menu principal...", style="yellow")
            break
        else:
            console.print("Opção inválida.", style="bold red")
            input("\nPressione Enter para tentar novamente.")
