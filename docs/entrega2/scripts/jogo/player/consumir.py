# jogo/player/consumir.py

from jogo.db import get_db_connection
from rich.console import Console

# Inicializa o console da Rich
console = Console()

def consumir_item(id_instancia_item, id_estudante):
    """
    Consome um item do inventário do jogador.
    Se for 'Consumível', reduz o estresse.
    Se for 'Monetário', aumenta o dinheiro.
    """
    # Importa a função de verificação aqui para evitar importação circular
    from .menu import check_emoji_support
    EMOJI_SUPPORT = check_emoji_support()
    icon_success = "✅" if EMOJI_SUPPORT else "[v]"
    icon_error = "❌" if EMOJI_SUPPORT else "[x]"

    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            # 1. Verifica o tipo do item
            cur.execute("""
                SELECT ti.item_tipo
                FROM instancia_de_item ii
                JOIN tipo_item ti ON ii.id_item = ti.id_item
                WHERE ii.id_instanciaItem = %s AND ii.id_estudante = %s;
            """, (id_instancia_item, id_estudante))
            
            item_info = cur.fetchone()
            if not item_info:
                console.print(f"{icon_error} Item não encontrado no inventário.", style="bold red")
                return

            item_tipo = item_info[0].strip()

            # 2. Executa a ação baseada no tipo
            if item_tipo == 'Consumível':
                # Lógica para reduzir estresse
                cur.execute("SELECT c.efeito, c.nome FROM instancia_de_item ci JOIN consumivel c ON ci.id_item = c.id_item WHERE ci.id_instanciaItem = %s;", (id_instancia_item,))
                efeito, nome_item = cur.fetchone()
                cur.execute("UPDATE estudante SET estresse = GREATEST(estresse - %s, 0) WHERE id_estudante = %s RETURNING estresse;", (efeito, id_estudante))
                novo_estresse = cur.fetchone()[0]
                console.print(f"{icon_success} Item '[bold magenta]{nome_item.strip()}[/bold magenta]' consumido! Estresse atual: {novo_estresse}")

            elif item_tipo == 'Monetário':
                # Lógica para adicionar dinheiro
                cur.execute("SELECT m.valor, m.nome FROM instancia_de_item mi JOIN monetario m ON mi.id_item = m.id_item WHERE mi.id_instanciaItem = %s;", (id_instancia_item,))
                valor, nome_item = cur.fetchone()
                cur.execute("UPDATE estudante SET total_dinheiro = total_dinheiro + %s WHERE id_estudante = %s RETURNING total_dinheiro;", (valor, id_estudante))
                novo_dinheiro = cur.fetchone()[0]
                console.print(f"{icon_success} Item '[bold magenta]{nome_item.strip()}[/bold magenta]' usado! Dinheiro total: {novo_dinheiro}")

            else:
                console.print(f"{icon_error} Este tipo de item não pode ser consumido.", style="bold yellow")
                return

            # 3. Remove o item do inventário após o uso
            cur.execute("DELETE FROM instancia_de_item WHERE id_instanciaItem = %s;", (id_instancia_item,))
            conn.commit()

    except Exception as e:
        if conn:
            conn.rollback()
        console.print(f"Erro ao consumir item: {e}", style="bold red")

    finally:
        if conn:
            conn.close()
