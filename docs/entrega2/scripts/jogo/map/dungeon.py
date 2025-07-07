# jogo/map/dungeon.py

from jogo.db import get_db_connection, clear_screen
from psycopg2 import Error
from jogo.combate.main import iniciar_combate, recompensa
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

# Mapeamento manual do tema para o ID do boss
BOSS_POR_TEMA = {
    1: 11,  # Matemática
    2: 12,  # Programação
    3: 14,  # Engenharias
    4: 13,  # Humanidades
    5: 15   # Gerais
}

def _exibir_detalhes_dungeon(monstros, boss_info, id_dungeon):
    """Exibe os detalhes dos monstros e do chefe da dungeon em tabelas estilizadas."""
    clear_screen()
    
    # Painel do Boss
    if boss_info:
        id_criatura_boss, nome_boss, desc_boss, nivel_boss, vida_max_boss, id_reliquia, nome_reliquia = boss_info
        
        # CORREÇÃO: Usar Text.assemble para construir o texto com estilos
        boss_panel_text = Text.assemble(
            ("Descrição: ", "default"), (f"{desc_boss.strip()}\n", "white"),
            ("Nível: ", "default"), (str(nivel_boss), "bold yellow"), (" | Vida Máx: ", "default"), (str(vida_max_boss), "bold red"), "\n",
            ("Relíquia: ", "default"), (nome_reliquia.strip(), "bold magenta")
        )
        
        icon_boss = "🦹" if EMOJI_SUPPORT else ""
        console.print(Panel(boss_panel_text, title=f"{icon_boss} Boss: {nome_boss.strip()}", border_style="red"))
    else:
        console.print(Panel("[yellow]Nenhum boss encontrado para este tema.[/yellow]", title="Aviso"))

    # Tabela de Monstros
    if not monstros:
        console.print(Panel("[yellow]Nenhum monstro simples encontrado nesta dungeon.[/yellow]", title="Aviso"))
    else:
        monster_table = Table(title="Monstros na Dungeon", border_style="purple")
        monster_table.add_column("Nº", style="cyan", justify="center")
        monster_table.add_column("Nome", style="magenta")
        monster_table.add_column("Nível", style="yellow")
        monster_table.add_column("Vida", style="green")
        monster_table.add_column("XP", style="blue")
        monster_table.add_column("Moedas", style="gold1")
        
        for idx, m in enumerate(monstros, start=1):
            _, _, nome, _, nivel_m, vida_max_m, vida_atual, moedas, xp = m
            vida_str = f"{vida_atual}/{vida_max_m}"
            monster_table.add_row(str(idx), nome.strip(), str(nivel_m), vida_str, str(xp), str(moedas))
        console.print(monster_table)

def tem_dungeon_interativo(jogador):
    id_sala = jogador['id_sala']
    id_estudante = jogador['id']
    conn = None

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT s.tem_dungeon, d.id_dungeon, d.nome, d.descricao, d.id_tema, t.nome
            FROM sala_comum s
            JOIN dungeon_academica d ON d.id_dungeon = s.id_sala
            JOIN tema t ON d.id_tema = t.id_tema
            WHERE s.id_sala = %s
        """, (id_sala,))
        resultado = cur.fetchone()

        if not resultado or not resultado[0]:
            icon = "📭" if EMOJI_SUPPORT else ""
            console.print(f"\n{icon} [yellow]Esta sala não possui uma dungeon.[/yellow]")
            console.input("\n[dim]Pressione Enter para voltar...[/dim]")
            return False

        _, id_dungeon, nome_dungeon, descricao_dungeon, id_tema, tema_nome = resultado
        id_boss = BOSS_POR_TEMA.get(id_tema)

        boss_info = None
        if id_boss:
            cur.execute("""
                SELECT b.id_criatura, b.nome, b.descricao, b.nivel, b.vida_max, b.id_reliquia, r.nome
                FROM boss b JOIN reliquia r ON b.id_reliquia = r.id_reliquia
                WHERE b.id_criatura = %s
            """, (id_boss,))
            boss_info = cur.fetchone()

        disponivel = True
        if boss_info:
            cur.execute("SELECT 1 FROM instancia_de_item ii JOIN reliquia r ON ii.id_item = r.id_reliquia WHERE ii.id_estudante = %s AND r.id_reliquia = %s LIMIT 1", (id_estudante, boss_info[5]))
            disponivel = cur.fetchone() is None

        status_text = Text("Aberta", style="green") if disponivel else Text("Fechada (Você já possui a relíquia)", style="red")
        icon_dungeon = "🏰" if EMOJI_SUPPORT else ""
        
        # CORREÇÃO: Usar Text.assemble para construir o texto com estilos
        dungeon_panel_text = Text.assemble(
            ("Tema: ", "default"), (tema_nome.strip(), "bold blue"), "\n",
            ("Descrição: ", "default"), (f"{descricao_dungeon.strip()}\n", "white"),
            ("Status: ", "default"), status_text
        )

        clear_screen()
        console.print(Panel(dungeon_panel_text, title=f"{icon_dungeon} Dungeon: {nome_dungeon.strip()}", border_style="magenta"))

        if not disponivel:
            console.input("\n[dim]Pressione Enter para voltar...[/dim]")
            return True

        menu_table = Table(show_header=False, show_edge=False, box=None)
        menu_table.add_row("[bold cyan][1][/bold cyan]", "Ver detalhes do Boss e Monstros")
        menu_table.add_row("[bold cyan][2][/bold cyan]", "Voltar")
        console.print(Panel(menu_table, title="Ações"))
        
        escolha = console.input("\n[bold]Escolha uma opção: [/bold]").strip()

        if escolha == '1':
            cur.execute("""
                SELECT ic.id_instanciaCriatura, m.id_criatura, m.nome, m.descricao, m.nivel, m.vida_max,
                       ic.vida_atual, m.qtd_moedas, m.xp_tema
                FROM instancia_de_criatura ic
                JOIN monstro_simples m ON ic.id_criatura = m.id_criatura
                WHERE ic.id_dungeon = %s
            """, (id_dungeon,))
            monstros = cur.fetchall()
            
            _exibir_detalhes_dungeon(monstros, boss_info, id_dungeon)

            if not monstros:
                 console.input("\n[dim]Pressione Enter para voltar...[/dim]")
                 return True

            escolha_monstro_str = console.input("\n[bold]Digite o número do monstro para enfrentar ou 0 para voltar: [/bold]").strip()
            if escolha_monstro_str.isdigit():
                escolha_monstro = int(escolha_monstro_str)
                if escolha_monstro == 0:
                    console.print("[yellow]Voltando...[/yellow]")
                elif 1 <= escolha_monstro <= len(monstros):
                    monstro = monstros[escolha_monstro - 1]
                    id_inst_criatura = monstro[0]
                    icon_combat = "⚔️" if EMOJI_SUPPORT else ""
                    console.print(f"\n{icon_combat} Você escolheu enfrentar [bold magenta]{monstro[2].strip()}[/bold magenta]!")
                    console.input("\n[dim]Pressione Enter para iniciar o combate...[/dim]")

                    resultado, vida_restante = iniciar_combate(id_estudante, id_inst_criatura)
                    
                    icon_result = "🏆" if EMOJI_SUPPORT else ""
                    if resultado == 'vitoria':
                        console.print(f"{icon_result} [bold green]Você venceu o monstro![/bold green]")
                        recompensa(id_inst_criatura, id_estudante)
                    elif resultado == 'derrota':
                        icon_result = "💀" if EMOJI_SUPPORT else ""
                        console.print(f"{icon_result} [bold red]Você foi derrotado pelo monstro![/bold red]")
                    elif resultado == 'fugiu':
                        icon_result = "🏃" if EMOJI_SUPPORT else ""
                        console.print(f"{icon_result} [yellow]Você fugiu do combate![/yellow]")

                    console.input("\n[dim]Pressione Enter para continuar...[/dim]")
                else:
                    console.print("[bold red]Opção inválida.[/bold red]")
            else:
                console.print("[bold red]Entrada inválida.[/bold red]")
        else:
            console.print("[yellow]Voltando...[/yellow]")

        return True

    except Exception as e:
        icon_error = "❌" if EMOJI_SUPPORT else "[x]"
        console.print(f"{icon_error} [bold red]Erro ao acessar dungeon: {e}[/bold red]")
        return False

    finally:
        if conn:
            conn.close()
