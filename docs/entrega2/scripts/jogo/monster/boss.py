from jogo.db import get_db_connection, clear_screen

def buscar_boss_e_reliquia(id_dungeon):
    """Busca o boss e a relíquia da dungeon pelo id da dungeon (id_sala)."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        query = """
            SELECT
                b.id_criatura,
                b.nome,
                b.descricao,
                b.nivel,
                b.vida_max,
                r.id_reliquia,
                r.nome AS nome_reliquia,
                r.descricao AS desc_reliquia,
                r.tipo_reliquia,
                ic.id_instanciaCriatura,
                ic.vida_atual
            FROM instancia_de_criatura ic
            JOIN boss b ON b.id_criatura = ic.id_criatura
            JOIN reliquia r ON r.id_reliquia = b.id_reliquia
            WHERE ic.id_dungeon = %s
            LIMIT 1;
        """
        cur.execute(query, (id_dungeon,))
        resultado = cur.fetchone()
        return resultado  # Pode ser None se não houver boss
    except Exception as e:
        print(f"Erro ao buscar boss e relíquia: {e}")
        return None
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()