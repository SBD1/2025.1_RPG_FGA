# jogo/player/menu.py

import os # Módulo para verificar o sistema operacional
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from jogo.player.habilidades import *
from jogo.player.afinidade import *
from jogo.player.inventario import *
from jogo.map.sala import *
from jogo.map.setor import *
from jogo.db import clear_screen
from jogo.player.estresse import *

# Cria uma instância do Console da Rich para usar em todo o módulo
console = Console()

# ======== NOVA FUNÇÃO DE DETECÇÃO DE EMOJI ========
def check_emoji_support():
    """Verifica de forma mais robusta se o terminal suporta emojis."""
    # Se estiver no moderno Windows Terminal, o suporte é garantido.
    if os.environ.get("WT_SESSION"):
        return True
    # Se estiver no WSL, mas não no Windows Terminal, é provável que seja um terminal antigo.
    if os.environ.get("WSL_DISTRO_NAME"):
        return False
    # Para outros sistemas (Linux, macOS), o suporte é geralmente bom.
    if os.name != 'nt':
        return True
    # Para terminais antigos do Windows (CMD, PowerShell), o suporte é ruim.
    return False

# Verifica o suporte a emojis uma vez no início
EMOJI_SUPPORT = check_emoji_support()

def carregar_estudante(id_estudante):
    # (Esta função permanece a mesma)
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
        cur.close()
        conn.close()

# ======== BARRA DE ESTRESSE CORRIGIDA ========
def barra_estresse(estresse, max_estresse=100):
    """Cria uma barra de estresse com emojis ou caracteres de fallback como um objeto Text da Rich."""
    blocos = int((estresse / max_estresse) * 10)
    blocos = min(blocos, 10)
    vazios = 10 - blocos
    
    bar = Text()
    if EMOJI_SUPPORT:
        # Emojis para terminais compatíveis
        bar.append("🟧" * blocos)
        bar.append("⬛" * vazios)
    else:
        # Fallback para Windows CMD/PowerShell com cores
        bar.append("*" * blocos, style="bold red")
        bar.append("-" * vazios, style="white")
    return bar

def menu_jogador(jogador):
    # --- Lógica de ícones dinâmicos ---
    icon_player = "🎒 Jogador:" if EMOJI_SUPPORT else "Jogador:"
    icon_money = "💰 Dinheiro:" if EMOJI_SUPPORT else "Dinheiro:"
    icon_location = "📍 Local:" if EMOJI_SUPPORT else "Local:"
    icon_stress = "😰 " if EMOJI_SUPPORT else "Estresse:"
    icon_door = "🚪 ID:" if EMOJI_SUPPORT else "ID:"
    
    # Ícones para as opções do menu removidos.

    while True:
        jogador.update(carregar_estudante(jogador['id']))
        verifica_estresse(jogador)
        #input("\nPressione Enter para continuar.")

        clear_screen()

        # --- Painel de Status do Jogador (Lógica de construção corrigida) ---
        status_text = Text(justify="left")
        status_text.append(f"{icon_player} {jogador['nome']} | {icon_stress} [", style="bold white")
        status_text.append(barra_estresse(jogador['estresse'])) # Anexa o objeto Text da barra
        status_text.append(f"] {jogador['estresse']}/100\n", style="bold white")
        status_text.append(f"{icon_money} ", style="bold white")
        status_text.append(f"$ {jogador['total_dinheiro']}\n", style="bold gold1")
        status_text.append(f"{icon_location} ", style="bold white")
        status_text.append(f"{jogador['nome_sala']}")
        
        console.print(Panel(status_text, title="[bold cyan]STATUS[/bold cyan]", border_style="green"))

        # --- Tabela de Opções do Menu ---
        menu_table = Table(show_header=False, show_edge=False, box=None)
        menu_table.add_column(style="bold magenta")
        menu_table.add_column()

        menu_table.add_row("[1]", "Ver Habilidades")
        menu_table.add_row("[2]", "Ver Afinidades")
        menu_table.add_row("[3]", "Ver Inventário")
        menu_table.add_row("---", "------------------")
        menu_table.add_row("[4]", "Explorar Sala Atual")
        menu_table.add_row("[5]", "Mudar de Sala")
        menu_table.add_row("[6]", "Mudar de Setor")
        menu_table.add_row("---", "------------------")
        menu_table.add_row("[7]", "Sair para o Menu Principal")
        
        console.print(Panel(menu_table, title="[bold cyan]MENU[/bold cyan]", border_style="blue"))

        opcao = console.input("[bold]Escolha uma opção: [/bold]")

        # A lógica de cada opção continua a mesma...
        if opcao == '1':
            clear_screen()
            habilidades = buscar_habilidades_estudante_todas(jogador['id'])
            mostrar_catalogo_habilidades(habilidades)
            console.input("\n[dim]Pressione Enter para voltar...[/dim]")

        elif opcao == '2':
            clear_screen()
            mostrar_menu_afinidade(jogador)
            console.input("\n[dim]Pressione Enter para voltar...[/dim]")

        elif opcao == '3':
            clear_screen()
            menu_inventario(jogador)
            console.input("\n[dim]Pressione Enter para voltar...[/dim]")

        elif opcao == '4':
            explorar_sala(jogador)

        elif opcao == '5':
            clear_screen()
            salas = listar_salas(jogador['id'])
            if not salas:
                console.print("Nenhuma sala vizinha disponível.", style="bold red")
            else:
                salas_disponiveis_ids = {sala[0] for sala in salas}

                console.print("\n--- Salas Vizinhas Disponíveis  ---", style="bold yellow")
                
                for sala in salas:
                    console.print(f"\n[bold cyan]{icon_door} {sala[0]}[/bold cyan] - [bold]{sala[1]}[/bold]")
                    console.print(f"   ({sala[2]})")
                
                print("\n" + "="*40)
                
                try:
                    novo_id = int(console.input("\n[bold]Digite o ID da sala para onde deseja ir: [/bold]"))
                    
                    if novo_id in salas_disponiveis_ids:
                        sucesso = mover_estudante_para_sala(jogador['id'], novo_id)
                        if sucesso:
                            nova_sala_nome = next((s[1] for s in salas if s[0] == novo_id), "Sala Desconhecida")
                            jogador['id_sala'] = novo_id  
                            jogador['nome_sala'] = nova_sala_nome
                    else:
                        console.print("\nID inválido. Você só pode se mover para uma das salas listadas.", style="bold red")

                except ValueError:
                    print("\nEntrada inválida. Por favor, digite um número.", style="bold red")
            console.input("\n[dim]Pressione Enter para voltar...[/dim]")

        elif opcao == '6':
            clear_screen()
            nova_sala = mudar_setor_estudante(jogador['id'])
            if nova_sala:
                jogador['nome_sala'] = nova_sala
            console.input("\n[dim]Pressione Enter para voltar...[/dim]")

        elif opcao == '7':
            console.print("Retornando ao menu principal.", style="bold yellow")
            break

        else:
            console.print("Opção inválida. Tente novamente.", style="bold red")
            input("\nPressione Enter para tentar novamente.")
