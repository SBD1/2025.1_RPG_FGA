from jogo.db import get_db_connection, clear_screen

def buscar_monstros_simples(id_dungeon):
    """Busca os monstros simples da dungeon pelo id da dungeon (id_sala)."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        query = """
            SELECT
                ms.id_criatura,
                ms.nome,
                ms.descricao,
                ms.nivel,
                ms.vida_max,
                ms.xp_tema,
                ms.qtd_moedas,
                ic.id_instanciaCriatura,
                ic.vida_atual
            FROM instancia_de_criatura ic
            JOIN monstro_simples ms ON ms.id_criatura = ic.id_criatura
            WHERE ic.id_dungeon = %s;
        """
        cur.execute(query, (id_dungeon,))
        resultados = cur.fetchall()
        return resultados  # Lista de tuplas ou [] se nenhum monstro
    except Exception as e:
        print(f"Erro ao buscar monstros simples: {e}")
        return []
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
