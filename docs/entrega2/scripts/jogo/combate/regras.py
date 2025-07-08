# jogo/combate/regras.py

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import os

console = Console()

# Função de verificação de emoji local
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

# Dicionário de eficácias permanece o mesmo
eficacias = {
    'M': {'P': 1.5, 'H': 0.75}, 'P': {'E': 1.5, 'M': 0.75},
    'H': {'M': 1.5, 'G': 0.75}, 'E': {'G': 1.5, 'P': 0.75},
    'G': {'H': 1.5, 'E': 0.75}
}

def eficacia(elemento1, elemento2):
    """(Nome e corpo da função mantidos)."""
    return eficacias.get(elemento1, {}).get(elemento2, 1)

def mostrar_eficacia(mult, quem=''):
    """
    Exibe a mensagem de eficácia com estilo Rich e emojis condicionais.
    """
    icon_super = "🔥 " if EMOJI_SUPPORT else ""
    icon_poco = "💧 " if EMOJI_SUPPORT else ""
    
    if mult > 1:
        return Text.assemble((icon_super, "default"), (f"{quem} foi super efetivo!", "bold green"), f" (x{mult:.2f})\n")
    elif mult < 1:
        return Text.assemble((icon_poco, "default"), (f"{quem} foi pouco efetivo.", "bold yellow"), f" (x{mult:.2f})\n")
    else:
        return Text.assemble((f"{quem} teve eficácia neutra.", "default"), f" (x{mult:.2f})\n")

def aplicar_regras(j_acao, j_nome, j_hab, m_acao, m_nome, m_hab, vida_jogador, vida_monstro, vida_max_jogador, vida_max_monstro):
    """
    Aplica as regras e exibe o resultado em um painel Rich, com emojis condicionais.
    """
    log_combate = Text()
    
    # ===== INÍCIO DA CORREÇÃO DE EMOJIS =====
    # Define todos os ícones no início, com base no EMOJI_SUPPORT
    icon_player = "🧙 " if EMOJI_SUPPORT else ""
    icon_monster = "👹 " if EMOJI_SUPPORT else ""
    icon_dano = "💥 " if EMOJI_SUPPORT else ">> "
    icon_cura = "💖 " if EMOJI_SUPPORT else "++ "
    icon_defesa = "🛡️ " if EMOJI_SUPPORT else "|| "
    icon_cancel = "💔 " if EMOJI_SUPPORT else "!! "
    icon_block = "🧱 " if EMOJI_SUPPORT else "## "
    icon_alvo = "🎯 " if EMOJI_SUPPORT else "-> "
    # ===== FIM DA CORREÇÃO DE EMOJIS =====

    j_nome_str = j_nome if j_nome is not None else "Nenhuma Ação"
    m_nome_str = m_nome if m_nome is not None else "Nenhuma Ação"

    log_combate.append(Text.assemble((f"{icon_player}Jogador usou:  ", "default"), (j_acao.upper(), "bold magenta"), (" -> ", "default"), (j_nome_str, "cyan"), "\n"))
    log_combate.append(Text.assemble((f"{icon_monster}Monstro usou: ", "default"), (m_acao.upper(), "bold magenta"), (" -> ", "default"), (m_nome_str, "cyan"), "\n\n"))

    j_tipo, j_pot = j_hab['tipo'], j_hab['potencia']
    m_tipo, m_pot = m_hab['tipo'], m_hab['potencia']
    mult_j = eficacia(j_tipo, m_tipo)
    mult_m = eficacia(m_tipo, j_tipo)

    if j_acao == 'passar' and m_acao == 'passar':
        log_combate.append("Ambos passaram o turno. Nada aconteceu.\n")
    elif j_acao == 'passar':
        log_combate.append(f"{icon_player}Jogador passou o turno.\n")
        if m_acao == 'ataque': vida_jogador -= m_pot; log_combate.append(f"{icon_dano}Monstro causa {m_pot:.1f} de dano.\n")
        elif m_acao == 'cura': vida_monstro += m_pot; log_combate.append(f"{icon_cura}Monstro cura {m_pot:.1f} de vida.\n")
        elif m_acao == 'defesa': log_combate.append(f"{icon_defesa}Monstro se defendeu.\n")
    elif m_acao == 'passar':
        log_combate.append(f"{icon_monster}Monstro passou o turno.\n")
        if j_acao == 'ataque': vida_monstro -= j_pot; log_combate.append(f"{icon_dano}Jogador causa {j_pot:.1f} de dano.\n")
        elif j_acao == 'cura': vida_jogador += j_pot; log_combate.append(f"{icon_cura}Jogador cura {j_pot:.1f} de vida.\n")
        elif j_acao == 'defesa': log_combate.append(f"{icon_defesa}Jogador se defendeu.\n")
    else:
        if j_acao == 'ataque' and m_acao == 'ataque':
            dano_j = j_pot * mult_j; dano_m = m_pot * mult_m
            vida_monstro -= dano_j; vida_jogador -= dano_m
            log_combate.append(mostrar_eficacia(mult_j, "Jogador"))
            log_combate.append(mostrar_eficacia(mult_m, "Monstro"))
            log_combate.append(f"{icon_dano}Jogador causa {dano_j:.1f} de dano.\n")
            log_combate.append(f"{icon_dano}Monstro causa {dano_m:.1f} de dano.\n")
        elif j_acao == 'ataque' and m_acao == 'defesa':
            dano = max(0, (j_pot * mult_j) - (m_pot * mult_m))
            vida_monstro -= dano
            log_combate.append(mostrar_eficacia(mult_j, "Jogador"))
            log_combate.append(mostrar_eficacia(mult_m, "Monstro"))
            log_combate.append(f"{icon_defesa}Defesa do monstro absorveu {m_pot * mult_m:.1f} de dano.\n")
            log_combate.append(f"{icon_alvo}Dano final no monstro: {dano:.1f}.\n")
        elif j_acao == 'defesa' and m_acao == 'ataque':
            dano = max(0, (m_pot * mult_m) - (j_pot * mult_j))
            vida_jogador -= dano
            log_combate.append(mostrar_eficacia(mult_m, "Monstro"))
            log_combate.append(mostrar_eficacia(mult_j, "Jogador"))
            log_combate.append(f"{icon_defesa}Defesa do jogador absorveu {j_pot * mult_j:.1f} de dano.\n")
            log_combate.append(f"{icon_alvo}Dano final no jogador: {dano:.1f}.\n")
        elif j_acao == 'ataque' and m_acao == 'cura':
            dano = j_pot * mult_j
            vida_monstro -= dano
            log_combate.append(mostrar_eficacia(mult_j, "Jogador"))
            log_combate.append(f"{icon_cancel}O ataque do jogador cancelou a cura do monstro!\n")
            log_combate.append(f"{icon_dano}Jogador causa {dano:.1f} de dano.\n")
        elif j_acao == 'cura' and m_acao == 'ataque':
            dano = m_pot * mult_m
            vida_jogador -= dano
            log_combate.append(mostrar_eficacia(mult_m, "Monstro"))
            log_combate.append(f"{icon_cancel}O ataque do monstro cancelou a cura do jogador!\n")
            log_combate.append(f"{icon_dano}Monstro causa {dano:.1f} de dano.\n")
        elif j_acao == 'cura' and m_acao == 'cura':
            cura_j = j_pot * mult_j; cura_m = m_pot * mult_m
            vida_jogador += cura_j; vida_monstro += cura_m
            log_combate.append(mostrar_eficacia(mult_j, "Jogador"))
            log_combate.append(mostrar_eficacia(mult_m, "Monstro"))
            log_combate.append(f"{icon_cura}Jogador curou {cura_j:.1f} de vida.\n")
            log_combate.append(f"{icon_cura}Monstro curou {cura_m:.1f} de vida.\n")
        elif j_acao == 'defesa' and m_acao == 'defesa':
            log_combate.append(f"{icon_block}Ambos defenderam. Nada aconteceu.\n")
        elif j_acao == 'cura' and m_acao == 'defesa':
            cura_j = j_pot * mult_j
            vida_jogador += cura_j
            log_combate.append(mostrar_eficacia(mult_j, "Jogador"))
            log_combate.append(f"{icon_cura}Jogador curou {cura_j:.1f} de vida.\n")
            log_combate.append(f"{icon_defesa}Monstro se defendeu em vão.\n")
        elif j_acao == 'defesa' and m_acao == 'cura':
            cura_m = m_pot * mult_m
            vida_monstro += cura_m
            log_combate.append(mostrar_eficacia(mult_m, "Monstro"))
            log_combate.append(f"{icon_cura}Monstro curou {cura_m:.1f} de vida.\n")
            log_combate.append(f"{icon_defesa}Jogador se defendeu em vão.\n")

    vida_jogador = min(max(vida_jogador, 0), vida_max_jogador)
    vida_monstro = min(max(vida_monstro, 0), vida_max_monstro)
    
    console.print(Panel(log_combate, title="[bold yellow]Resultado do Turno[/bold yellow]", border_style="green", expand=True))
    console.input("\n[dim]Pressione Enter para continuar...[/dim]")
    
    return vida_jogador, vida_monstro