# jogo/reset.py

import os
from .db import get_db_connection
from rich.console import Console
from rich.panel import Panel
# Importa a função de verificação de emoji do menu do jogador
from .player.menu import check_emoji_support

# Inicializa o console da Rich e verifica o suporte a emojis
console = Console()
EMOJI_SUPPORT = check_emoji_support()

# Comando SQL para limpar todas as tabelas
TRUNCATE_TABLES_SQL = """
TRUNCATE TABLE
    tema, tipoHabilidade, tipo_criatura, campus, setor, sala_comum,
    estudante, afinidade, dungeon_academica, tipo_item, reliquia, boss,
    monstro_simples, instancia_de_criatura, consumivel, equipavel,
    monetario, loja_item, habilidade_criatura, habilidade_estudante,
    habilidade_loja, instancia_de_item, "ataque", "cura", "defesa"
RESTART IDENTITY CASCADE;
"""

def _execute_sql_file(cur, file_path):
    """Lê e executa o conteúdo de um arquivo .sql, com feedback estilizado."""
    icon_success = "✅" if EMOJI_SUPPORT else "[v]"
    icon_error = "❌" if EMOJI_SUPPORT else "[x]"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            sql_script = f.read()
            cur.execute(sql_script)
            console.print(f"{icon_success} Script '[bold cyan]{os.path.basename(file_path)}[/bold cyan]' executado com sucesso.")
    except FileNotFoundError:
        console.print(f"{icon_error} ERRO: Arquivo de script não encontrado em: [bold red]{file_path}[/bold red]")
        raise
    except Exception as e:
        console.print(f"{icon_error} ERRO ao executar o script '[bold red]{os.path.basename(file_path)}[/bold red]': {e}")
        raise

def reiniciar_banco_de_dados():
    """Limpa todas as tabelas e repopula o banco de dados com feedback visual."""
    # Define os ícones com base no suporte do terminal
    icon_progress = "⏳" if EMOJI_SUPPORT else "..."
    icon_success = "✅" if EMOJI_SUPPORT else "[v]"
    icon_party = "🎉" if EMOJI_SUPPORT else "!!!"

    conn = None
    try:
        console.print(f"\n[yellow]{icon_progress} Iniciando a reinicialização do banco de dados...[/yellow]")
        conn = get_db_connection()
        cur = conn.cursor()

        console.print("[cyan]1/4 - Desabilitando regras de sessão...[/cyan]")
        cur.execute("SET session_replication_role = 'replica';")

        console.print("[cyan]2/4 - Limpando todas as tabelas...[/cyan]")
        cur.execute(TRUNCATE_TABLES_SQL)
        console.print(f"{icon_success} Tabelas limpas e contadores de ID reiniciados.")
        
        console.print("[cyan]3/4 - Reabilitando regras de sessão...[/cyan]")
        cur.execute("SET session_replication_role = 'origin';")

        console.print("[cyan]4/4 - Repopulando o banco de dados...[/cyan]")
        dml_path = os.path.join(os.path.dirname(__file__), '..', 'DML.sql')
        _execute_sql_file(cur, os.path.normpath(dml_path))
        
        conn.commit()
        console.print(Panel(f"[bold green]{icon_party} Banco de dados reiniciado com sucesso![/bold green]", title="[bold green]Concluído[/bold green]", border_style="green"))

    except Exception as e:
        if conn:
            conn.rollback()
        console.print(Panel(f"[bold red]A reinicialização falhou:[/bold red]\n{e}", title="[bold red]Erro[/bold red]", border_style="red"))
    finally:
        if conn:
            conn.close()
