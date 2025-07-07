from jogo.db import get_db_connection
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# A importação problemática foi removida daqui.

# Inicializa o console da Rich
console = Console()

def buscar_habilidades_estudante_todas(id_estudante):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        query = """
        SELECT
            he.id_habilidade,
            th.tipo_habilidade,
            COALESCE(a.nome, c.nome, d.nome) AS nome,
            COALESCE(a.nivel, c.nivel, d.nivel) AS nivel,
            COALESCE(a.coolDown, c.coolDown, d.coolDown) AS cooldown,
            a.danoCausado,
            c.vidaRecuperada,
            d.danoMitigado,
            tm.nome AS nome_tema
        FROM habilidade_estudante he
        JOIN tipoHabilidade th ON he.id_habilidade = th.id_habilidade
        LEFT JOIN Ataque a ON he.id_habilidade = a.id_habilidade
        LEFT JOIN Cura c ON he.id_habilidade = c.id_habilidade
        LEFT JOIN Defesa d ON he.id_habilidade = d.id_habilidade
        LEFT JOIN tema tm ON COALESCE(a.id_tema, c.id_tema, d.id_tema) = tm.id_tema
        WHERE he.id_estudante = %s;
        """
        cur.execute(query, (id_estudante,))
        rows = cur.fetchall()
        
        habilidades = []
        for row in rows:
            nome_habilidade = row[2].strip() if row[2] else ''
            tipo = row[1].strip().lower() if row[1] else ''
            nome_tema = row[8].strip() if row[8] else 'N/A'
            # define potência conforme tipo
            if tipo == 'ataque':
                potencia = row[5]
            elif tipo == 'cura':
                potencia = row[6]
            elif tipo == 'defesa':
                potencia = row[7]
            else:
                potencia = None
            
            habilidades.append({
                'id_habilidade': row[0],
                'tipo_habilidade': tipo,
                'nome': nome_habilidade,
                'nivel': row[3],
                'cooldown': row[4],
                'potencia': potencia,
                'nome_tema': nome_tema
            })
        return habilidades
        
    except Exception as e:
        console.print(f"[bold red]Erro ao buscar habilidades: {e}[/bold red]")
        return []
    finally:
        if conn:
            cur.close()
            conn.close()

def mostrar_catalogo_habilidades(habilidades):
    """Exibe o catálogo de habilidades do jogador em uma tabela Rich."""
    
    # ======== CORREÇÃO DA IMPORTAÇÃO CIRCULAR ========
    # A importação é feita aqui, dentro da função, para evitar o erro.
    from .menu import check_emoji_support
    EMOJI_SUPPORT = check_emoji_support()
    
    icon_title = "🧠" if EMOJI_SUPPORT else ""
    
    if not habilidades:
        console.print(Panel("[yellow]Você ainda não possui nenhuma habilidade.[/yellow]", title="Aviso"))
        return

    # Cria a tabela para exibir as habilidades
    table = Table(title=f"{icon_title} Catálogo de Habilidades", border_style="blue")
    table.add_column("ID", style="cyan", justify="center")
    table.add_column("Nome", style="magenta", width=25)
    table.add_column("Tipo", style="green")
    table.add_column("Nível", style="yellow", justify="center")
    table.add_column("CD", style="red", justify="center")
    table.add_column("Potência", style="bold white", justify="center")
    table.add_column("Tema", style="blue")

    # Adiciona as habilidades à tabela
    for h in habilidades:
        potencia_str = str(h['potencia']) if h['potencia'] is not None else '-'
        table.add_row(
            str(h['id_habilidade']),
            h['nome'],
            h['tipo_habilidade'].capitalize(),
            str(h['nivel']),
            str(h['cooldown']),
            potencia_str,
            h['nome_tema']
        )
    
    console.print(table)
