# ===== main.py =====
import psycopg2
from rich.console import Console
from rich.panel import Panel

# Funções compatíveis com a nova estilização
from jogo.combate.inteligencia import escolher_acao_monstro
from jogo.combate.regras import aplicar_regras
from jogo.combate.combate import menu, escolher_habilidade, atualizar_cooldowns
import os
import sys
from jogo.db import get_db_connection
from jogo.monster.monster import * # <<< IMPORT ADICIONADO AQUI

console = Console()

def limpar_tela():
    """Função de limpeza mantida para compatibilidade."""
    try:
        from jogo.db import clear_screen as cs
        cs()
    except (ImportError, ModuleNotFoundError):
        os.system('cls' if os.name == 'nt' else 'clear')

# --- Funções de Carregamento (Nomes mantidos, 'print' trocado por 'console.print') ---

def carregar_habilidades_jogador(conn, id_jogador):
    # (Corpo original mantido, apenas a mensagem de erro foi estilizada)
    habilidades = {'ataque': {}, 'defesa': {}, 'cura': {}}
    try:
        with conn.cursor() as cur:
            # Sua query original aqui...
            cur.execute("""
                SELECT th.tipo_habilidade, COALESCE(a.nome, c.nome, d.nome), 
                       COALESCE(a.danoCausado, c.vidaRecuperada, d.danoMitigado), 
                       COALESCE(a.coolDown, c.coolDown, d.coolDown), t.nome
                FROM habilidade_estudante he
                JOIN tipoHabilidade th ON he.id_habilidade = th.id_habilidade
                LEFT JOIN Ataque a ON he.id_habilidade = a.id_habilidade 
                LEFT JOIN Cura c ON he.id_habilidade = c.id_habilidade 
                LEFT JOIN Defesa d ON he.id_habilidade = d.id_habilidade
                JOIN tema t ON COALESCE(a.id_tema, c.id_tema, d.id_tema) = t.id_tema
                WHERE he.id_estudante = %s
            """, (id_jogador,))
            for row in cur.fetchall():
                tipo_hab, nome, potencia, cooldown, tema = row
                if nome: # Garante que o nome não é nulo
                    habilidades[tipo_hab.lower().strip()][nome.strip()] = {
                        'tipo': tema[0].upper(), 'potencia': potencia, 'cooldown': cooldown
                    }
    except psycopg2.Error as e:
        console.print(f"[bold red]Erro ao carregar habilidades do jogador: {e}[/bold red]")
        return None
    return habilidades


def carregar_habilidades_monstro(conn, id_monstro):
    # (Corpo original mantido, apenas a mensagem de erro foi estilizada)
    habilidades = {'ataque': {}, 'defesa': {}, 'cura': {}}
    try:
        with conn.cursor() as cur:
            # Sua query original aqui...
            cur.execute("""
                SELECT th.tipo_habilidade, COALESCE(a.nome, c.nome, d.nome), 
                       COALESCE(a.danoCausado, c.vidaRecuperada, d.danoMitigado), 
                       COALESCE(a.coolDown, c.coolDown, d.coolDown), t.nome
                FROM habilidade_criatura hc
                JOIN tipoHabilidade th ON hc.id_habilidade = th.id_habilidade
                LEFT JOIN Ataque a ON hc.id_habilidade = a.id_habilidade 
                LEFT JOIN Cura c ON hc.id_habilidade = c.id_habilidade 
                LEFT JOIN Defesa d ON hc.id_habilidade = d.id_habilidade
                JOIN tema t ON COALESCE(a.id_tema, c.id_tema, d.id_tema) = t.id_tema
                WHERE hc.id_criatura = %s
            """, (id_monstro,))
            for row in cur.fetchall():
                tipo_hab, nome, potencia, cooldown, tema = row
                if nome: # Garante que o nome não é nulo
                    habilidades[tipo_hab.lower().strip()][nome.strip()] = {
                        'tipo': tema[0].upper(), 'potencia': potencia, 'cooldown': cooldown
                    }
    except psycopg2.Error as e:
        console.print(f"[bold red]Erro ao carregar habilidades do monstro: {e}[/bold red]")
        return None
    return habilidades


def carregar_vida_jogador(conn, id_jogador):
    # (Corpo original mantido, apenas a mensagem de erro foi estilizada)
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT vida FROM estudante WHERE id_estudante = %s", (id_jogador,))
            return cur.fetchone()[0]
    except (psycopg2.Error, TypeError) as e: 
        console.print(f"[bold red]Erro ao carregar vida do jogador: {e}[/bold red]")
        return 100

def carregar_vida_monstro(conn, id_monstro):
    # (Corpo original mantido, apenas a mensagem de erro foi estilizada)
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT vida_max FROM monstro_simples WHERE id_criatura = %s", (id_monstro,))
            return cur.fetchone()[0]
    except (psycopg2.Error, TypeError) as e:
        console.print(f"[bold red]Erro ao carregar vida do monstro: {e}[/bold red]")
        return 100


def iniciar_combate(id_jogador, id_monstro):
    """
    Função principal do combate, agora usando as funções estilizadas.
    (Nome e assinatura originais mantidos).
    """
    conn = get_db_connection()
    if not conn: return "erro", 0

    try:
        habilidades_jogador = carregar_habilidades_jogador(conn, id_jogador)
        habilidades_monstro = carregar_habilidades_monstro(conn, id_monstro)
        if not habilidades_jogador or not habilidades_monstro: return "erro", 0

        vida_max_jogador = vida_jogador = carregar_vida_jogador(conn, id_jogador)
        vida_max_monstro = vida_monstro = carregar_vida_monstro(conn, id_monstro)
        
        cooldowns_jogador, cooldowns_monstro = {}, {}
        mapa_acoes = {'A': 'ataque', 'D': 'defesa', 'C': 'cura'}

        while vida_jogador > 0 and vida_monstro > 0:
            limpar_tela()
            menu(vida_jogador, vida_monstro, vida_max_jogador, vida_max_monstro)
            entrada = console.input("[bold]Digite sua escolha: [/bold]").upper()

            if entrada == 'F':
                console.print(Panel("Você fugiu do combate!", style="yellow", title="Fuga"))
                return "fuga", vida_jogador
            
            if entrada == 'P':
                j_categoria, j_nome, j_habilidade = 'passar', 'Passar Turno', {'tipo': 'G', 'potencia': 0}
            elif entrada in mapa_acoes:
                j_categoria = mapa_acoes[entrada]
                j_nome, j_habilidade = escolher_habilidade(j_categoria, habilidades_jogador, cooldowns_jogador, vida_jogador, vida_monstro)
                
                if (j_nome, j_habilidade) == ("voltar", "voltar"): continue
                if j_nome is None:
                    console.input("\n[dim]Pressione Enter para voltar ao menu de ações...[/dim]")
                    continue
            else:
                console.print("[bold red]Opção inválida.[/bold red]")
                console.input("\n[dim]Pressione Enter para tentar novamente...[/dim]")
                continue

            m_categoria, (m_nome, m_habilidade) = escolher_acao_monstro(habilidades_monstro, vida_monstro, vida_jogador, cooldowns_monstro, j_categoria, j_habilidade['tipo'])
            if m_nome is None: m_categoria, m_nome, m_habilidade = 'passar', 'Passar Turno', {'tipo': 'G', 'potencia': 0}

            limpar_tela()
            vida_jogador, vida_monstro = aplicar_regras(j_categoria, j_nome, j_habilidade, m_categoria, m_nome, m_habilidade, vida_jogador, vida_monstro, vida_max_jogador, vida_max_monstro)
            
            if j_categoria != 'passar': cooldowns_jogador[j_nome] = j_habilidade.get('cooldown', 0)
            if m_categoria != 'passar': cooldowns_monstro[m_nome] = m_habilidade.get('cooldown', 0)
            
            atualizar_cooldowns(cooldowns_jogador)
            atualizar_cooldowns(cooldowns_monstro)

        # Resultados do combate
        limpar_tela()
        if vida_jogador <= 0:
            console.print(Panel("Você foi derrotado!", title="[bold red]Fim de Combate[/bold red]"))
            return "derrota", 0
        else: # Vitória ou Fuga
            console.print(Panel("Vitória! Você derrotou o monstro!", title="[bold green]Fim de Combate[/bold green]"))
            return "vitoria", vida_jogador

    except (psycopg2.Error, TypeError) as e:
        console.print(Panel(f"Erro crítico durante o combate: {e}", title="[bold red]ERRO[/bold red]"))
        return "erro", 0
    finally:
        if conn: conn.close()