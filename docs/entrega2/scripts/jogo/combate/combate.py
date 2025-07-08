# jogo/combate/combate.py

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
import os

console = Console()

def _check_emoji_support():
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

EMOJI_SUPPORT = _check_emoji_support()

def barra_vida(vida_atual, vida_maxima, nome):
    total_blocos = 20
    proporcao = vida_atual / vida_maxima if vida_maxima > 0 else 0
    blocos_cheios = int(proporcao * total_blocos)
    blocos_vazios = total_blocos - blocos_cheios
    cor_barra = "green" if proporcao > 0.5 else "yellow" if proporcao > 0.2 else "red"
    bar = Text()

    if EMOJI_SUPPORT:
        bar.append("🟥" * blocos_cheios); bar.append("⬛" * blocos_vazios)
    else:
        bar.append("=" * blocos_cheios, style=f"bold {cor_barra}"); bar.append("-" * blocos_vazios, style="white")
    return Text.assemble(f"{nome}: [", bar, f"] {vida_atual:.0f}/{vida_maxima}")

def menu(vida_jogador, vida_monstro, vida_max_jogador, vida_max_monstro):
    icon_player = "🧙 " if EMOJI_SUPPORT else ""
    icon_monster = "👹 " if EMOJI_SUPPORT else ""

    barra_jogador_txt = barra_vida(vida_jogador, vida_max_jogador, f"{icon_player}Jogador")
    barra_monstro_txt = barra_vida(vida_monstro, vida_max_monstro, f"{icon_monster}Monstro")

    status_content = Text("\n").join([barra_jogador_txt, barra_monstro_txt])

    console.print(Panel(status_content, title="[bold cyan]HORA DO DUELO[/bold cyan]", border_style="red"))

    action_table = Table(show_header=False, show_edge=False, box=None)
    action_table.add_column(style="bold magenta", justify="right")
    action_table.add_column()
    action_table.add_row("[A]", "Habilidade de Ataque")
    action_table.add_row("[D]", "Habilidade de Defesa")
    action_table.add_row("[C]", "Habilidade de Cura")
    action_table.add_row("[P]", "Passar o turno")
    action_table.add_row("[F]", "Fugir")
    console.print(Panel(action_table, title="[bold yellow]Escolha sua Ação[/bold yellow]", border_style="blue"))

def lista_habilidades_com_cooldown(habilidades_dict, cooldowns):
    tipo_emojis = {"M": "📐 ", "P": "💻 ", "E": "⚙️ ", "H": "📚 ", "G": "🌐 "}

    table = Table(show_header=True, header_style="bold purple")

    table.add_column("Nº", style="cyan")
    table.add_column("Nome", style="magenta", width=25)
    table.add_column("Potência", style="yellow")
    table.add_column("Tema", style="blue")
    table.add_column("Status", style="green")
    habilidades_lista = list(habilidades_dict.items())

    for i, (nome, detalhes) in enumerate(habilidades_lista, 1):
        cooldown = cooldowns.get(nome, 0)
        status = f"[bold red](Cooldown: {cooldown})[/bold red]" if cooldown > 0 else "[bold green]Pronta[/bold green]"
        emoji = tipo_emojis.get(detalhes['tipo'], "❓ ") if EMOJI_SUPPORT else ''
        table.add_row(f"[{i}]", nome, str(detalhes['potencia']), f"{emoji}{detalhes['tipo']}", status)
    console.print(table)

def escolher_habilidade(categoria, habilidades, cooldowns, vida_jogador, vida_monstro):
    if EMOJI_SUPPORT:
        mapa_icones = {"ataque": "💥 ", "defesa": "🛡️ ", "cura": "💖 "}
    else:
        mapa_icones = {"ataque": "", "defesa": "", "cura": ""}

    icon = mapa_icones.get(categoria.lower(), "✨ " if EMOJI_SUPPORT else "")

    console.print(Panel(f"[bold cyan]{icon}MENU DE {categoria.upper()}[/bold cyan]", border_style="purple"))

    habilidades_categoria = habilidades.get(categoria, {})
    lista_habilidades_com_cooldown(habilidades_categoria, cooldowns)
    disponiveis = [(nome, det) for nome, det in habilidades_categoria.items() if cooldowns.get(nome, 0) == 0]
    
    if not disponiveis:
        console.print("\n[yellow]Todas as habilidades desta categoria estão em cooldown.[/yellow]")
        return None, None 
    while True:
        try:
            escolha_str = console.input("[bold]Escolha a habilidade pelo número (ou 0 para voltar): [/bold]")
            escolha = int(escolha_str)
            if escolha == 0: return "voltar", "voltar"
            if 1 <= escolha <= len(habilidades_categoria):
                nome_escolhido, detalhes_escolhidos = list(habilidades_categoria.items())[escolha - 1]
                if cooldowns.get(nome_escolhido, 0) > 0:
                    console.print("[bold red]Essa habilidade está em cooldown. Escolha outra.[/bold red]")
                    continue
                return nome_escolhido, detalhes_escolhidos
            else: console.print("[bold red]Opção inválida. Tente novamente.[/bold red]")
        except ValueError: console.print("[bold red]Entrada inválida. Digite um número.[/bold red]")

def atualizar_cooldowns(cooldowns):
    for habilidade in list(cooldowns):
        cooldowns[habilidade] -= 1
        if cooldowns[habilidade] <= 0: del cooldowns[habilidade]