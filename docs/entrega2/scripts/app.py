import sys
import os
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Importa as funções necessárias dos outros módulos
from jogo.player.menu import menu_jogador, check_emoji_support
from jogo.db import get_db_connection, clear_screen
from jogo.reset import reiniciar_banco_de_dados
from jogo.debug_menu import menu_debug_queries

# Inicializa o console da Rich e verifica o suporte a emojis
console = Console()
EMOJI_SUPPORT = check_emoji_support()

def listar_estudantes_disponiveis():
    conn = get_db_connection()
    if not conn:
        console.print("Não foi possível conectar ao banco.", style="bold red")
        return []
    try:
        cur = conn.cursor()
        cur.execute("SELECT id_estudante, nome FROM estudante ORDER BY id_estudante")
        estudantes = cur.fetchall()
        estudantes = [(id_, nome.strip()) for id_, nome in estudantes]
        return estudantes
    except Exception as e:
        console.print(f"Erro ao buscar estudantes: {e}", style="bold red")
        return []
    finally:
        if conn:
            cur.close()
            conn.close()

def carregar_dados_estudante(id_estudante):
    # Esta função não precisa de alterações visuais
    conn = get_db_connection()
    if not conn:
        print("Não foi possível conectar ao banco.")
        return None
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT e.nome, e.vida, e.estresse, e.total_dinheiro, s.nome AS nome_sala, e.id_sala
            FROM estudante e
            JOIN sala_comum s ON e.id_sala = s.id_sala
            WHERE e.id_estudante = %s
        """, (id_estudante,))
        resultado = cur.fetchone()
        if not resultado:
            print("Estudante não encontrado.")
            return None
        
        nome, vida, estresse, total_dinheiro, nome_sala, id_sala = resultado
        return {
            "id": id_estudante,
            "nome": nome.strip(),
            "vida": vida,
            "estresse": estresse,
            "total_dinheiro": total_dinheiro,
            "nome_sala": nome_sala.strip(),
            "id_sala": id_sala
        }
    except Exception as e:
        print("Erro ao carregar dados do estudante:", e)
        return None
    finally:
        if conn:
            cur.close()
            conn.close()
    
# ======== MENU PRINCIPAL ESTILIZADO COM RICH ========
def menu_principal():
    # Define ícones condicionais para o menu
    icon_student = "🎓" if EMOJI_SUPPORT else ""
    icon_wave = "👋" if EMOJI_SUPPORT else ""

    while True:
        clear_screen()
        
        # Título do Jogo em um Painel
        console.print(Panel("RPG FGA", title="[bold green]Bem-vindo ao[/bold green]", border_style="magenta"), justify="center")

        # Tabela de Opções
        menu_table = Table(show_header=False, show_edge=False, box=None)
        menu_table.add_column(style="bold magenta", justify="right")
        menu_table.add_column(justify="left")
        
        menu_table.add_row("[1]", "Selecionar Personagem")
        menu_table.add_row("[2]", "Créditos")
        menu_table.add_row("[3]", "Reiniciar Jogo")
        menu_table.add_row("[4]", "Menu de Debug")
        menu_table.add_row("[5]", "Sair do Jogo")
        
        console.print(Panel(menu_table, title="[bold cyan]MENU INICIAL[/bold cyan]", border_style="blue"))

        opcao = console.input("[bold]Escolha uma opção: [/bold]")

        if opcao == "1":
            clear_screen()
            estudantes = listar_estudantes_disponiveis()
            if not estudantes:
                console.print("\nNenhum estudante disponível. Talvez o banco precise ser reiniciado?", style="yellow")
                input("\nPressione Enter para continuar...")
                continue
            
            # Exibe estudantes em uma tabela estilizada
            student_table = Table(title=f"{icon_student} Estudantes Disponíveis", border_style="green")
            student_table.add_column("ID", style="cyan")
            student_table.add_column("Nome", style="magenta")
            for id_, nome in estudantes:
                student_table.add_row(str(id_), nome)
            
            console.print(student_table)
            
            escolhido = console.input("\n[bold]Digite o ID do estudante: [/bold]")
            if not escolhido.isdigit():
                console.print("ID inválido.", style="bold red")
                input("\nPressione Enter para continuar...")
                continue
            jogador = carregar_dados_estudante(int(escolhido))
            if jogador:
                menu_jogador(jogador)
        
        elif opcao == "2":
            clear_screen()
            console.print(Panel("Jogo desenvolvido por Rafael e IA da OpenAI 😎", title="[bold yellow]Créditos[/bold yellow]"))
            input("\nPressione Enter para voltar ao menu.")

        elif opcao == "3":
            clear_screen()
            console.print(Panel("Esta ação apagará TODOS os dados salvos e recomeçará o jogo do zero.", title="[bold red]ATENÇÃO![/bold red]"))
            confirmacao = console.input("Digite [bold yellow]'CONFIRMAR'[/bold yellow] para continuar ou qualquer outra coisa para cancelar: ")
            
            if confirmacao == "CONFIRMAR":
                reiniciar_banco_de_dados()
            else:
                console.print("\nOperação cancelada.", style="yellow")
            
            input("\nPressione Enter para voltar ao menu principal.")

        elif opcao == "4":
            menu_debug_queries()

        elif opcao == "5":
            console.print(f"\n{icon_wave} Saindo do jogo...", style="bold yellow")
            sys.exit()
        else:
            console.print("Opção inválida.", style="bold red")
            input("\nPressione Enter para continuar...")


if __name__ == "__main__":
    menu_principal()
