# jogo/debug_menu.py

from .db import get_db_connection, clear_screen
from psycopg2 import Error
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from .player.menu import check_emoji_support
# Importa a função necessária de afinidade
from .player.afinidade import carregar_afinidades_estudante

# Inicializa o console e verifica o suporte a emojis
console = Console()
EMOJI_SUPPORT = check_emoji_support()

# --- Funções de Cheat Movidas e Melhoradas ---

def _listar_estudantes_para_cheat():
    """Busca e exibe uma lista de todos os estudantes para o menu de cheat."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id_estudante, nome FROM estudante ORDER BY id_estudante")
        estudantes = cur.fetchall()
        
        if not estudantes:
            console.print("[yellow]Nenhum estudante encontrado no banco de dados.[/yellow]")
            return None

        table = Table(title="Selecione o Jogador para Editar", border_style="yellow")
        table.add_column("ID", style="cyan")
        table.add_column("Nome", style="magenta")
        for id_estudante, nome in estudantes:
            table.add_row(str(id_estudante), nome.strip())
        console.print(table)
        return estudantes
    except Exception as e:
        console.print(f"[bold red]Erro ao listar estudantes: {e}[/bold red]")
        return None
    finally:
        if conn: conn.close()

def _alterar_nivel_afinidade(id_estudante, nome_estudante):
    """Lida com a lógica de alterar o nível de uma afinidade."""
    clear_screen()
    console.print(Panel(f"Alterando afinidades de [bold magenta]{nome_estudante}[/bold magenta]", border_style="yellow"))
    
    afinidades = carregar_afinidades_estudante(id_estudante)
    if not afinidades:
        console.print("[yellow]Nenhuma afinidade encontrada para este estudante.[/yellow]")
        return

    table = Table(title="Selecione a Afinidade para Alterar", border_style="yellow")
    table.add_column("Opção", style="cyan")
    table.add_column("Tema", style="magenta")
    table.add_column("Nível Atual", style="green")
    for idx, a in enumerate(afinidades, 1):
        table.add_row(f"[{idx}]", a['nome_tema'], str(a['nivel']))
    console.print(table)

    escolha_afinidade = console.input("\n[bold]Escolha a afinidade (ou 0 para cancelar): [/bold]").strip()
    if not escolha_afinidade.isdigit() or int(escolha_afinidade) == 0: return
    
    try:
        idx_afinidade = int(escolha_afinidade) - 1
        if not 0 <= idx_afinidade < len(afinidades): raise ValueError
        afinidade_selecionada = afinidades[idx_afinidade]
        
        nivel_novo_str = console.input(f"[bold]Digite o novo nível para '{afinidade_selecionada['nome_tema']}' (1 a 20): [/bold]").strip()
        nivel_novo = int(nivel_novo_str)
        if not 1 <= nivel_novo <= 20: raise ValueError

        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute("UPDATE afinidade SET nivel_atual = %s, xp_atual = 0 WHERE id_estudante = %s AND id_tema = %s", (nivel_novo, id_estudante, afinidade_selecionada['id_tema']))
            conn.commit()
        console.print(f"[green]Nível da afinidade '{afinidade_selecionada['nome_tema']}' atualizado para {nivel_novo} e XP zerado.[/green]")
    except (ValueError, IndexError):
        console.print("[bold red]Entrada inválida.[/bold red]")
    except Exception as e:
        console.print(f"[bold red]Erro ao atualizar nível: {e}[/bold red]")
    finally:
        if conn: conn.close()

def _adicionar_dinheiro(id_estudante, nome_estudante):
    """Adiciona uma quantia de dinheiro para o estudante selecionado."""
    clear_screen()
    console.print(Panel(f"Adicionando dinheiro para [bold magenta]{nome_estudante}[/bold magenta]", border_style="yellow"))
    
    try:
        quantia_str = console.input("[bold]Digite a quantia de dinheiro a ser adicionada: [/bold]").strip()
        quantia = int(quantia_str)

        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute("UPDATE estudante SET total_dinheiro = total_dinheiro + %s WHERE id_estudante = %s", (quantia, id_estudante))
            conn.commit()
        console.print(f"[green]{quantia} de dinheiro adicionado com sucesso![/green]")
    except ValueError:
        console.print("[bold red]Entrada inválida. Por favor, digite um número.[/bold red]")
    except Exception as e:
        console.print(f"[bold red]Erro ao adicionar dinheiro: {e}[/bold red]")
    finally:
        if conn: conn.close()

def cheat_menu():
    """Menu principal de cheats, começando pela seleção do jogador."""
    clear_screen()
    console.print(Panel("[bold yellow]Cheat Menu[/bold yellow]", border_style="red", subtitle="Selecione um jogador para editar"))
    
    estudantes = _listar_estudantes_para_cheat()
    if not estudantes:
        console.input("\n[dim]Pressione Enter para continuar...[/dim]")
        return

    id_escolhido = console.input("\n[bold]Digite o ID do estudante (ou 0 para cancelar): [/bold]").strip()
    if not id_escolhido.isdigit() or id_escolhido == '0': return

    try:
        id_estudante = int(id_escolhido)
        estudante_selecionado = next((e for e in estudantes if e[0] == id_estudante), None)
        if not estudante_selecionado:
            console.print("[bold red]ID de estudante inválido.[/bold red]")
            console.input("\n[dim]Pressione Enter para continuar...[/dim]")
            return
        
        nome_estudante = estudante_selecionado[1].strip()

        while True:
            clear_screen()
            submenu_table = Table(show_header=False, show_edge=False, box=None)
            submenu_table.add_column(style="bold cyan", justify="right")
            submenu_table.add_column(justify="left")
            submenu_table.add_row("[1]", "Alterar Nível de Afinidade")
            submenu_table.add_row("[2]", "Adicionar Dinheiro")
            submenu_table.add_row("[3]", "Voltar")
            
            console.print(Panel(submenu_table, title=f"Editando [bold magenta]{nome_estudante}[/bold magenta]", border_style="yellow"))
            
            opcao = console.input("[bold]Escolha uma opção: [/bold]").strip()
            
            if opcao == '1':
                _alterar_nivel_afinidade(id_estudante, nome_estudante)
                console.input("\n[dim]Pressione Enter para continuar...[/dim]")
            elif opcao == '2':
                _adicionar_dinheiro(id_estudante, nome_estudante)
                console.input("\n[dim]Pressione Enter para continuar...[/dim]")
            elif opcao == '3':
                break
            else:
                console.print("[bold red]Opção inválida.[/bold red]")
                console.input("\n[dim]Pressione Enter para continuar...[/dim]")

    except (ValueError, IndexError):
        console.print("[bold red]Entrada inválida.[/bold red]")
        console.input("\n[dim]Pressione Enter para continuar...[/dim]")

# --- Funções de Listagem do Debug Menu (sem alterações) ---

def listar_salas_com_dungeon():
    clear_screen()
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT s.id_sala, s.nome, st.nome AS nome_setor FROM sala_comum s JOIN setor st ON s.id_setor = st.id_setor WHERE s.tem_dungeon = TRUE ORDER BY s.id_sala;")
        salas = cur.fetchall()
        title = "🏰 Salas com Dungeon" if EMOJI_SUPPORT else "Salas com Dungeon"
        table = Table(title=title, border_style="cyan")
        table.add_column("ID Sala", style="magenta")
        table.add_column("Nome da Sala", style="green")
        table.add_column("Setor", style="yellow")
        if not salas: console.print(Panel("[yellow]Nenhuma sala com dungeon encontrada.[/yellow]", title="Resultado"))
        else:
            for sala in salas: table.add_row(str(sala[0]), sala[1].strip(), sala[2].strip())
            console.print(table)
        cur.close()
        conn.close()
    except (Exception, Error) as e: console.print(f"[bold red]Erro ao buscar salas com dungeon: {e}[/bold red]")
    console.input("\n[dim]Pressione Enter para voltar...[/dim]")

def listar_salas_com_loja():
    clear_screen()
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT s.id_sala, s.nome, st.nome AS nome_setor FROM sala_comum s JOIN setor st ON s.id_setor = st.id_setor WHERE s.tem_loja = TRUE ORDER BY s.id_sala;")
        salas = cur.fetchall()
        title = "🏪 Salas com Loja" if EMOJI_SUPPORT else "Salas com Loja"
        table = Table(title=title, border_style="cyan")
        table.add_column("ID Sala", style="magenta")
        table.add_column("Nome da Sala", style="green")
        table.add_column("Setor", style="yellow")
        if not salas: console.print(Panel("[yellow]Nenhuma sala com loja encontrada.[/yellow]", title="Resultado"))
        else:
            for sala in salas: table.add_row(str(sala[0]), sala[1].strip(), sala[2].strip())
            console.print(table)
        cur.close()
        conn.close()
    except (Exception, Error) as e: console.print(f"[bold red]Erro ao buscar salas com loja: {e}[/bold red]")
    console.input("\n[dim]Pressione Enter para voltar...[/dim]")

def listar_salas_com_itens():
    clear_screen()
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT s.id_sala, s.nome, COUNT(ii.id_instanciaItem) AS quantidade_itens FROM sala_comum s JOIN instancia_de_item ii ON s.id_sala = ii.id_sala WHERE ii.id_estudante IS NULL GROUP BY s.id_sala, s.nome ORDER BY s.id_sala;")
        salas = cur.fetchall()
        title = "✨ Salas com Itens no Chão" if EMOJI_SUPPORT else "Salas com Itens no Chão"
        table = Table(title=title, border_style="cyan")
        table.add_column("ID Sala", style="magenta")
        table.add_column("Nome da Sala", style="green")
        table.add_column("Qtd. de Itens", style="yellow")
        if not salas: console.print(Panel("[yellow]Nenhuma sala com itens no chão encontrada.[/yellow]", title="Resultado"))
        else:
            for sala in salas: table.add_row(str(sala[0]), sala[1].strip(), str(sala[2]))
            console.print(table)
        cur.close()
        conn.close()
    except (Exception, Error) as e: console.print(f"[bold red]Erro ao buscar salas com itens: {e}[/bold red]")
    console.input("\n[dim]Pressione Enter para voltar...[/dim]")

def listar_posicao_jogadores():
    clear_screen()
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT e.nome, s.nome, st.nome FROM estudante e JOIN sala_comum s ON e.id_sala = s.id_sala JOIN setor st ON s.id_setor = st.id_setor ORDER BY e.id_estudante;")
        jogadores = cur.fetchall()
        title = "📍 Posição dos Jogadores" if EMOJI_SUPPORT else "Posição dos Jogadores"
        table = Table(title=title, border_style="cyan")
        table.add_column("Jogador", style="magenta")
        table.add_column("Sala Atual", style="green")
        table.add_column("Setor", style="yellow")
        if not jogadores: console.print(Panel("[yellow]Nenhum jogador encontrado.[/yellow]", title="Resultado"))
        else:
            for jogador in jogadores: table.add_row(jogador[0].strip(), jogador[1].strip(), jogador[2].strip())
            console.print(table)
        cur.close()
        conn.close()
    except (Exception, Error) as e: console.print(f"[bold red]Erro ao buscar a posição dos jogadores: {e}[/bold red]")
    console.input("\n[dim]Pressione Enter para voltar...[/dim]")

def listar_detalhes_dungeons():
    clear_screen()
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT s.id_sala, s.nome, d.nome, t.nome FROM sala_comum s JOIN dungeon_academica d ON d.id_dungeon = s.id_sala JOIN tema t ON d.id_tema = t.id_tema ORDER BY s.id_sala;")
        dungeons = cur.fetchall()
        title = "📜 Detalhes das Dungeons" if EMOJI_SUPPORT else "Detalhes das Dungeons"
        table = Table(title=title, border_style="cyan")
        table.add_column("ID Sala", style="magenta")
        table.add_column("Nome da Sala", style="green")
        table.add_column("Nome da Dungeon", style="yellow")
        table.add_column("Tema", style="blue")
        if not dungeons: console.print(Panel("[yellow]Nenhuma dungeon encontrada.[/yellow]", title="Resultado"))
        else:
            for dungeon in dungeons: table.add_row(str(dungeon[0]), dungeon[1].strip(), dungeon[2].strip(), dungeon[3].strip())
            console.print(table)
        cur.close()
        conn.close()
    except (Exception, Error) as e: console.print(f"[bold red]Erro ao buscar detalhes das dungeons: {e}[/bold red]")
    console.input("\n[dim]Pressione Enter para voltar...[/dim]")


def menu_debug_queries():
    """Exibe o menu de consultas de debug estilizado com Rich."""
    icon_dungeon = "🏰" if EMOJI_SUPPORT else ""
    icon_shop = "🏪" if EMOJI_SUPPORT else ""
    icon_item = "✨" if EMOJI_SUPPORT else ""
    icon_player = "📍" if EMOJI_SUPPORT else ""
    icon_details = "📜" if EMOJI_SUPPORT else ""
    icon_cheat = "🔧" if EMOJI_SUPPORT else ""
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
        menu_table.add_row("[6]", f" {icon_cheat} Menu de Cheats") # <<-- OPÇÃO ATUALIZADA
        menu_table.add_row("[7]", f" {icon_back} Voltar ao Menu Principal")
        
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
            cheat_menu()
        elif opcao == '7':
            console.print("Retornando ao menu principal...", style="yellow")
            break
        else:
            console.print("Opção inválida.", style="bold red")
            input("\nPressione Enter para tentar novamente.")
