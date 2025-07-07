# jogo/player/inventario.py

from jogo.db import get_db_connection, clear_screen
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# Importa as funções de ação
from .equipar import atualizar_status_equipavel
from .consumir import consumir_item

# Inicializa o console da Rich
console = Console()

# --- Funções de Busca (sem alterações na lógica interna) ---

def buscar_consumiveis(id_estudante):
    query = "SELECT ci.id_instanciaItem, c.nome, c.descricao, c.efeito FROM instancia_de_item ci JOIN consumivel c ON ci.id_item = c.id_item WHERE ci.id_estudante = %s;"
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute(query, (id_estudante,))
            return [{'id_instanciaItem': r[0], 'nome_item': r[1].strip(), 'descricao': r[2].strip(), 'efeito': r[3]} for r in cur.fetchall()]
    except Exception as e:
        console.print(f"[bold red]Erro ao buscar consumíveis: {e}[/bold red]")
        return []
    finally:
        if conn: conn.close()

def buscar_equipaveis(id_estudante):
    query = "SELECT ei.id_instanciaItem, e.nome, e.descricao, e.efeito, ei.equipado FROM instancia_de_item ei JOIN equipavel e ON ei.id_item = e.id_item WHERE ei.id_estudante = %s;"
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute(query, (id_estudante,))
            return [{'id_instanciaItem': r[0], 'nome_item': r[1].strip(), 'descricao': r[2].strip(), 'efeito': r[3], 'equipado': r[4]} for r in cur.fetchall()]
    except Exception as e:
        console.print(f"[bold red]Erro ao buscar equipáveis: {e}[/bold red]")
        return []
    finally:
        if conn: conn.close()

def buscar_reliquias(id_estudante):
    query = "SELECT ri.id_instanciaItem, r.nome, r.descricao, r.tipo_reliquia FROM instancia_de_item ri JOIN reliquia r ON ri.id_item = r.id_reliquia WHERE ri.id_estudante = %s;"
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute(query, (id_estudante,))
            return [{'id_instanciaItem': r[0], 'nome_reliquia': r[1].strip(), 'descricao': r[2].strip(), 'tipo_reliquia': r[3].strip()} for r in cur.fetchall()]
    except Exception as e:
        console.print(f"[bold red]Erro ao buscar relíquias: {e}[/bold red]")
        return []
    finally:
        if conn: conn.close()

def buscar_monetarios(id_estudante):
    query = "SELECT mi.id_instanciaItem, m.nome, m.descricao, m.valor FROM instancia_de_item mi JOIN monetario m ON mi.id_item = m.id_item WHERE mi.id_estudante = %s;"
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute(query, (id_estudante,))
            return [{'id_instanciaItem': r[0], 'nome_item': r[1].strip(), 'descricao': r[2].strip(), 'valor': r[3]} for r in cur.fetchall()]
    except Exception as e:
        console.print(f"[bold red]Erro ao buscar itens monetários: {e}[/bold red]")
        return []
    finally:
        if conn: conn.close()

# --- Submenus de Categoria Estilizados ---

def _menu_consumiveis(jogador):
    """Exibe e gerencia a categoria de itens consumíveis."""
    from .menu import check_emoji_support
    EMOJI_SUPPORT = check_emoji_support()
    icon_title = "🧪" if EMOJI_SUPPORT else ""
    icon_error = "❌" if EMOJI_SUPPORT else "[x]"
    
    clear_screen()
    itens = buscar_consumiveis(jogador['id'])
    
    table = Table(title=f"{icon_title} Consumíveis", border_style="green")
    table.add_column("ID", style="cyan")
    table.add_column("Nome", style="magenta")
    table.add_column("Efeito", style="yellow")
    table.add_column("Descrição", style="white")

    if not itens:
        console.print(Panel("[yellow]Nenhum item consumível encontrado.[/yellow]", title="Aviso"))
    else:
        for item in itens:
            table.add_row(str(item['id_instanciaItem']), item['nome_item'], str(item['efeito']), item['descricao'])
        console.print(table)

        console.print("\n[bold][1][/bold] Consumir um item")
        console.print("[bold][2][/bold] Voltar")
        opcao = console.input("\n[bold]Escolha uma ação: [/bold]")

        if opcao == '1':
            try:
                id_item_str = console.input('[bold]Informe o ID do item que deseja consumir: [/bold]')
                if not id_item_str.isdigit(): raise ValueError
                id_item = int(id_item_str)
                if any(i['id_instanciaItem'] == id_item for i in itens):
                    consumir_item(id_item, jogador['id'])
                else:
                    console.print(f"{icon_error} ID inválido. Nenhum item encontrado com esse ID.", style="bold red")
            except ValueError:
                console.print(f"{icon_error} Entrada inválida. Por favor, informe um número.", style="bold red")

def _menu_equipaveis(jogador):
    """Exibe e gerencia a categoria de itens equipáveis."""
    from .menu import check_emoji_support
    EMOJI_SUPPORT = check_emoji_support()
    icon_title = "⚔️" if EMOJI_SUPPORT else ""
    icon_error = "❌" if EMOJI_SUPPORT else "[x]"
    
    clear_screen()
    itens = buscar_equipaveis(jogador['id'])

    table = Table(title=f"{icon_title} Equipáveis", border_style="blue")
    table.add_column("ID", style="cyan")
    table.add_column("Nome", style="magenta")
    table.add_column("Efeito", style="yellow")
    table.add_column("Descrição", style="white")
    table.add_column("Status", style="green")

    if not itens:
        console.print(Panel("[yellow]Nenhum item equipável encontrado.[/yellow]", title="Aviso"))
    else:
        for item in itens:
            status = "[green]Equipado[/green]" if item['equipado'] else "[red]Não Equipado[/red]"
            table.add_row(str(item['id_instanciaItem']), item['nome_item'], str(item['efeito']), item['descricao'], status)
        console.print(table)

        console.print("\n[bold][1][/bold] Equipar/Desequipar um item")
        console.print("[bold][2][/bold] Voltar")
        opcao = console.input("\n[bold]Escolha uma ação: [/bold]")

        if opcao == '1':
            try:
                id_escolhido_str = console.input('[bold]Informe o ID do item: [/bold]')
                if not id_escolhido_str.isdigit(): raise ValueError
                id_escolhido = int(id_escolhido_str)
                if any(i['id_instanciaItem'] == id_escolhido for i in itens):
                    atualizar_status_equipavel(id_escolhido)
                else:
                    console.print(f"{icon_error} ID inválido. Nenhum item encontrado com esse ID.", style="bold red")
            except ValueError:
                console.print(f"{icon_error} Entrada inválida. Por favor, informe um número.", style="bold red")

def _mostrar_reliquias(id_estudante):
    """Exibe as relíquias do jogador."""
    from .menu import check_emoji_support
    EMOJI_SUPPORT = check_emoji_support()
    icon_title = "📜" if EMOJI_SUPPORT else ""
    
    clear_screen()
    itens = buscar_reliquias(id_estudante)
    
    table = Table(title=f"{icon_title} Relíquias", border_style="yellow")
    table.add_column("ID", style="cyan")
    table.add_column("Nome", style="magenta")
    table.add_column("Tipo", style="green")
    table.add_column("Descrição", style="white")

    if not itens:
        console.print(Panel("[yellow]Nenhuma relíquia encontrada.[/yellow]", title="Aviso"))
    else:
        for item in itens:
            table.add_row(str(item['id_instanciaItem']), item['nome_reliquia'], item['tipo_reliquia'], item['descricao'])
        console.print(table)

def _menu_monetarios(jogador):
    """Exibe e gerencia a categoria de itens monetários."""
    from .menu import check_emoji_support
    EMOJI_SUPPORT = check_emoji_support()
    icon_title = "💰" if EMOJI_SUPPORT else "$"
    icon_error = "❌" if EMOJI_SUPPORT else "[x]"
    
    clear_screen()
    itens = buscar_monetarios(jogador['id'])

    table = Table(title=f"{icon_title} Itens Monetários", border_style="purple")
    table.add_column("ID", style="cyan")
    table.add_column("Nome", style="magenta")
    table.add_column("Valor", style="yellow")
    table.add_column("Descrição", style="white")

    if not itens:
        console.print(Panel("[yellow]Nenhum item monetário encontrado.[/yellow]", title="Aviso"))
    else:
        for item in itens:
            table.add_row(str(item['id_instanciaItem']), item['nome_item'], str(item['valor']), item['descricao'])
        console.print(table)
        
        console.print("\n[bold][1][/bold] Usar item")
        console.print("[bold][2][/bold] Voltar")
        opcao = console.input("\n[bold]Escolha uma ação: [/bold]")

        if opcao == '1':
            try:
                id_item_str = console.input('[bold]Informe o ID do item que deseja usar: [/bold]')
                if not id_item_str.isdigit(): raise ValueError
                id_item = int(id_item_str)
                if any(i['id_instanciaItem'] == id_item for i in itens):
                    consumir_item(id_item, jogador['id'])
                else:
                    console.print(f"{icon_error} ID inválido. Nenhum item encontrado com esse ID.", style="bold red")
            except ValueError:
                console.print(f"{icon_error} Entrada inválida. Por favor, informe um número.", style="bold red")

# --- Menu Principal do Inventário Estilizado ---

def menu_inventario(jogador):
    """Exibe o menu principal do inventário."""
    from .menu import check_emoji_support
    EMOJI_SUPPORT = check_emoji_support()
    
    icon_consumable = "🧪" if EMOJI_SUPPORT else ""
    icon_equipable = "⚔️" if EMOJI_SUPPORT else ""
    icon_relic = "📜" if EMOJI_SUPPORT else ""
    icon_money = "💰" if EMOJI_SUPPORT else ""
    icon_back = "↩️" if EMOJI_SUPPORT else ""
    icon_error = "❌" if EMOJI_SUPPORT else "[x]"

    while True:
        clear_screen()
        
        menu_table = Table(show_header=False, show_edge=False, box=None)
        menu_table.add_column(style="bold magenta", justify="right")
        menu_table.add_column(justify="left")

        menu_table.add_row("[1]", f" {icon_consumable} Consumíveis")
        menu_table.add_row("[2]", f" {icon_equipable} Equipáveis")
        menu_table.add_row("[3]", f" {icon_relic} Relíquias")
        menu_table.add_row("[4]", f" {icon_money} Monetários")
        menu_table.add_row("[5]", f" {icon_back} Voltar")

        console.print(Panel(menu_table, title="[bold cyan]Inventário[/bold cyan]", border_style="blue"))
        opcao = console.input("\n[bold]Escolha uma categoria: [/bold]")

        if opcao == '1':
            _menu_consumiveis(jogador)
            console.input("\n[dim]Pressione Enter para voltar...[/dim]")
        elif opcao == '2':
            _menu_equipaveis(jogador)
            console.input("\n[dim]Pressione Enter para voltar...[/dim]")
        elif opcao == '3':
            _mostrar_reliquias(jogador['id'])
            console.input("\n[dim]Pressione Enter para voltar...[/dim]")
        elif opcao == '4':
            _menu_monetarios(jogador)
            console.input("\n[dim]Pressione Enter para voltar...[/dim]")
        elif opcao == '5':
            break
        else:
            console.print(f"{icon_error} Opção inválida.", style="bold red")
            input("\nPressione Enter para tentar novamente.")
