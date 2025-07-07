# jogo/map/loja.py

from jogo.db import get_db_connection, clear_screen
from psycopg2 import Error
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

# Inicializa o console e a função de verificação de emoji
console = Console()

def _check_emoji_support():
    """Função de verificação de emoji para evitar importação circular."""
    import os
    if os.environ.get("WT_SESSION"):
        return True
    if os.environ.get("WSL_DISTRO_NAME"):
        return False
    if os.name != 'nt':
        return True
    return False

EMOJI_SUPPORT = _check_emoji_support()

EMOJIS_TEMA_ID = {
    1: '📐', 2: '💻', 3: '⚙️', 4: '📚', 5: '🌐',
}

def exibir_itens_e_habilidades(id_loja, cur):
    """Exibe os itens e habilidades disponíveis na loja em tabelas Rich."""
    icon_shop = "🏪" if EMOJI_SUPPORT else ""
    icon_item = "🧪" if EMOJI_SUPPORT else ""
    icon_skill = "🧠" if EMOJI_SUPPORT else ""

    # Busca consumíveis
    cur.execute("""
        SELECT i.id_item, c.nome, c.descricao, c.preco, c.efeito
        FROM loja_item li
        JOIN tipo_item i ON li.id_item = i.id_item
        JOIN consumivel c ON i.id_item = c.id_item
        WHERE li.id_sala = %s;
    """, (id_loja,))
    itens = cur.fetchall()

    # Busca habilidades
    cur.execute("""
        SELECT th.id_habilidade, COALESCE(a.nome, c.nome, d.nome) AS nome, th.tipo_habilidade,
               COALESCE(a.preco, c.preco, d.preco) AS preco, t.nome AS nome_tema,
               COALESCE(a.nivel, c.nivel, d.nivel) AS nivel_req, t.id_tema
        FROM habilidade_loja hl
        JOIN tipoHabilidade th ON hl.id_habilidade = th.id_habilidade
        LEFT JOIN Ataque a ON hl.id_habilidade = a.id_habilidade
        LEFT JOIN Cura c ON hl.id_habilidade = c.id_habilidade
        LEFT JOIN Defesa d ON hl.id_habilidade = d.id_habilidade
        LEFT JOIN tema t ON COALESCE(a.id_tema, c.id_tema, d.id_tema) = t.id_tema
        WHERE hl.id_loja = %s;
    """, (id_loja,))
    habilidades = cur.fetchall()

    clear_screen()
    console.print(Panel(f"[bold green]{icon_shop} BEM-VINDO À LOJA! {icon_shop}[/bold green]", border_style="yellow"))

    if not itens and not habilidades:
        console.print(Panel("[yellow]Esta loja está vazia no momento.[/yellow]", title="Aviso"))
        return [], []

    # Tabela de Itens
    item_table = Table(title=f"{icon_item} Itens à Venda", border_style="green")
    item_table.add_column("ID", style="cyan")
    item_table.add_column("Nome", style="magenta")
    item_table.add_column("Preço", style="yellow")
    item_table.add_column("Efeito", style="bold green")
    item_table.add_column("Descrição", style="white")
    if itens:
        for item in itens:
            item_table.add_row(str(item[0]), item[1].strip(), str(item[3]), f"{item[4]} Estresse", item[2].strip())
        console.print(item_table)

    # Tabela de Habilidades
    skill_table = Table(title=f"{icon_skill} Habilidades à Venda", border_style="blue")
    skill_table.add_column("ID", style="cyan")
    skill_table.add_column("Nome", style="magenta")
    skill_table.add_column("Tipo", style="green")
    skill_table.add_column("Tema", style="blue")
    skill_table.add_column("Nível Req.", style="yellow")
    skill_table.add_column("Preço", style="yellow")
    if habilidades:
        for hab in habilidades:
            if hab[3] is None: continue
            skill_table.add_row(str(hab[0]), hab[1].strip(), hab[2].strip().capitalize(), hab[4].strip(), str(hab[5]), str(hab[3]))
        console.print(skill_table)

    return itens, habilidades

def comprar_item(jogador, item, conn, cur):
    """Realiza a compra de um item com feedback estilizado."""
    icon_success = "✅" if EMOJI_SUPPORT else "[v]"
    icon_error = "❌" if EMOJI_SUPPORT else "[x]"
    id_estudante = jogador['id']
    id_item, nome_item, _, preco_item, _ = item

    if jogador['total_dinheiro'] < preco_item:
        console.print(f"{icon_error} [bold red]Dinheiro insuficiente![/bold red]")
        return

    nova_quantia = jogador['total_dinheiro'] - preco_item
    cur.execute("UPDATE estudante SET total_dinheiro = %s WHERE id_estudante = %s", (nova_quantia, id_estudante))
    cur.execute("INSERT INTO instancia_de_item (id_estudante, id_item) VALUES (%s, %s)", (id_estudante, id_item))
    conn.commit()
    jogador['total_dinheiro'] = nova_quantia
    console.print(f"{icon_success} Você comprou '[bold magenta]{nome_item.strip()}[/bold magenta]'!")

def comprar_habilidade(jogador, habilidade, conn, cur):
    """Realiza a compra de uma habilidade com feedback estilizado."""
    icon_success = "✅" if EMOJI_SUPPORT else "[v]"
    icon_error = "❌" if EMOJI_SUPPORT else "[x]"
    id_estudante = jogador['id']
    id_habilidade, nome_habilidade, _, preco_habilidade, nome_tema, nivel_req, id_tema = habilidade

    cur.execute("SELECT nivel_atual FROM afinidade WHERE id_estudante = %s AND id_tema = %s", (id_estudante, id_tema))
    resultado_afinidade = cur.fetchone()
    nivel_jogador_no_tema = resultado_afinidade[0] if resultado_afinidade else 0

    if nivel_jogador_no_tema < nivel_req:
        console.print(f"\n{icon_error} [bold red]Nível insuficiente no tema '{nome_tema.strip()}'![/bold red]")
        console.print(f"   Nível requerido: {nivel_req} | Seu nível: {nivel_jogador_no_tema}")
        return

    if jogador['total_dinheiro'] < preco_habilidade:
        console.print(f"{icon_error} [bold red]Dinheiro insuficiente![/bold red]")
        return

    cur.execute("SELECT 1 FROM habilidade_estudante WHERE id_estudante = %s AND id_habilidade = %s", (id_estudante, id_habilidade))
    if cur.fetchone():
        console.print(f"{icon_error} [bold yellow]Você já possui esta habilidade.[/bold yellow]")
        return

    nova_quantia = jogador['total_dinheiro'] - preco_habilidade
    cur.execute("UPDATE estudante SET total_dinheiro = %s WHERE id_estudante = %s", (nova_quantia, id_estudante))
    cur.execute("INSERT INTO habilidade_estudante (id_estudante, id_habilidade) VALUES (%s, %s)", (id_estudante, id_habilidade))
    conn.commit()
    jogador['total_dinheiro'] = nova_quantia
    console.print(f"{icon_success} Você aprendeu a habilidade '[bold magenta]{nome_habilidade.strip()}[/bold magenta]'!")

def acessar_loja(jogador):
    """Função principal para acessar e interagir com a loja."""
    id_sala = jogador['id_sala']
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT tem_loja FROM sala_comum WHERE id_sala = %s", (id_sala,))
        resultado = cur.fetchone()

        if not resultado or not resultado[0]:
            console.print("\n[yellow]Esta sala não possui uma loja.[/yellow]")
            console.input("\n[dim]Pressione Enter para voltar...[/dim]")
            return

        id_loja = id_sala 

        while True:
            itens, habilidades = exibir_itens_e_habilidades(id_loja, cur)
            
            # Busca e exibe os níveis de afinidade do jogador
            cur.execute("SELECT t.id_tema, t.nome, a.nivel_atual FROM afinidade a JOIN tema t ON a.id_tema = t.id_tema WHERE a.id_estudante = %s ORDER BY t.id_tema;", (jogador['id'],))
            afinidades = cur.fetchall()
            
            # CORREÇÃO: Usar Text.assemble para garantir a formatação correta
            afinidades_parts = []
            for id_tema, nome_tema, nivel in afinidades:
                emoji = EMOJIS_TEMA_ID.get(id_tema, " ") if EMOJI_SUPPORT else ""
                # Adiciona cada parte como uma tupla (texto, estilo) ou apenas texto
                afinidades_parts.append(f"{emoji} {nome_tema.strip()}: ")
                afinidades_parts.append((str(nivel), "bold yellow"))
                afinidades_parts.append(" | ")
            
            # Remove o último separador
            if afinidades_parts:
                afinidades_parts.pop()

            afinidades_text = Text.assemble(*afinidades_parts, justify="center")

            console.print(Panel(afinidades_text, title="Seus Níveis de Afinidade"))

            icon_money = "💰" if EMOJI_SUPPORT else "$"
            console.print(f"\nSeu dinheiro: [bold gold1]{icon_money} {jogador['total_dinheiro']}[/bold gold1]")
            
            menu_acoes = Table(show_header=False, show_edge=False, box=None)
            menu_acoes.add_column(style="bold cyan", justify="right")
            menu_acoes.add_column()
            menu_acoes.add_row("[I]", "Comprar Item")
            menu_acoes.add_row("[H]", "Comprar Habilidade")
            menu_acoes.add_row("[S]", "Sair da Loja")
            console.print(Panel(menu_acoes, title="Ações"))

            escolha = console.input("[bold]Escolha uma opção: [/bold]").strip().upper()

            if escolha == 'S':
                console.print("[yellow]Até mais![/yellow]")
                break
            
            elif escolha == 'I':
                if not itens:
                    console.print("[yellow]Não há itens para comprar.[/yellow]")
                else:
                    try:
                        id_compra = int(console.input("[bold]Digite o ID do item que deseja comprar: [/bold]"))
                        item_selecionado = next((item for item in itens if item[0] == id_compra), None)
                        if item_selecionado:
                            comprar_item(jogador, item_selecionado, conn, cur)
                        else:
                            console.print("[bold red]ID de item inválido.[/bold red]")
                    except ValueError:
                        console.print("[bold red]Entrada inválida.[/bold red]")
                console.input("\n[dim]Pressione Enter para continuar...[/dim]")

            elif escolha == 'H':
                if not habilidades:
                    console.print("[yellow]Não há habilidades para comprar.[/yellow]")
                else:
                    try:
                        id_compra = int(console.input("[bold]Digite o ID da habilidade que deseja comprar: [/bold]"))
                        habilidade_selecionada = next((hab for hab in habilidades if hab[0] == id_compra), None)
                        if habilidade_selecionada:
                            comprar_habilidade(jogador, habilidade_selecionada, conn, cur)
                        else:
                            console.print("[bold red]ID de habilidade inválido.[/bold red]")
                    except ValueError:
                        console.print("[bold red]Entrada inválida.[/bold red]")
                console.input("\n[dim]Pressione Enter para continuar...[/dim]")
                
            else:
                console.print("[bold red]Opção inválida.[/bold red]")
                console.input("\n[dim]Pressione Enter para tentar novamente...[/dim]")

    except (Exception, Error) as e:
        if conn: conn.rollback()
        icon_error = "❌" if EMOJI_SUPPORT else "[x]"
        console.print(f"{icon_error} [bold red]Erro ao acessar a loja: {e}[/bold red]")
        console.input("\n[dim]Pressione Enter para voltar...[/dim]")
    finally:
        if conn: conn.close()
