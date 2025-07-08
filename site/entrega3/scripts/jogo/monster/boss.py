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



def recompensa_boss(id_boss, id_jogador):
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            # Busca a relíquia associada ao boss
            cur.execute("""
                SELECT id_reliquia
                FROM boss
                WHERE id_criatura = %s
            """, (id_boss,))
            resultado = cur.fetchone()

            if not resultado:
                print("❌ Boss não encontrado ou sem relíquia associada.")
                return False

            id_reliquia = resultado[0]

            # Cria nova instância de item (relíquia)
            cur.execute("""
                INSERT INTO instancia_de_item (id_item, id_estudante)
                VALUES (%s, %s)
            """, (id_reliquia, id_jogador))

            conn.commit()
            print("🎁 Relíquia conquistada com sucesso!")

            return True

    except Exception as e:
        print(f"❌ Erro ao gerar recompensa do boss: {e}")
        return False

    finally:
        if conn:
            conn.close()