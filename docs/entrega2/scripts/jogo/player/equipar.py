# jogo/player/equipar.py

from jogo.db import get_db_connection
from rich.console import Console

# Inicializa o console da Rich
console = Console()

def atualizar_status_equipavel(id_instancia_item):
    """Atualiza o status 'equipado' de um item no banco de dados com feedback estilizado."""
    # Importa a função de verificação aqui para evitar importação circular
    from .menu import check_emoji_support
    EMOJI_SUPPORT = check_emoji_support()
    icon_success = "✅" if EMOJI_SUPPORT else "[v]"
    
    query_status = "SELECT equipado, e.nome FROM instancia_de_item i JOIN equipavel e ON i.id_item = e.id_item WHERE i.id_instanciaItem = %s;"
    query_update = "UPDATE instancia_de_item SET equipado = NOT equipado WHERE id_instanciaItem = %s;"
    
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            # Pega o status atual e o nome para o feedback
            cur.execute(query_status, (id_instancia_item,))
            status_atual, nome_item = cur.fetchone()
            nome_item = nome_item.strip()
            
            # Atualiza o item
            cur.execute(query_update, (id_instancia_item,))
            conn.commit()

            # Exibe a mensagem com base na ação realizada
            if not status_atual: # Se estava False, agora está True (equipou)
                console.print(f"{icon_success} Item '[bold magenta]{nome_item}[/bold magenta]' equipado com sucesso.")
            else: # Se estava True, agora está False (desequipou)
                console.print(f"{icon_success} Item '[bold magenta]{nome_item}[/bold magenta]' desequipado com sucesso.")
    except Exception as e:
        if conn: conn.rollback()
        console.print(f"[bold red]Erro ao atualizar status do item: {e}[/bold red]")
    finally:
        if conn:
            conn.close()
