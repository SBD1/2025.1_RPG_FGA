from jogo.db import get_db_connection

def consumir_item(id_instancia_item, id_estudante):
    query_efeito = """
        SELECT c.efeito
        FROM instancia_de_item ci
        JOIN consumivel c ON ci.id_item = c.id_item
        WHERE ci.id_instanciaItem = %s
          AND ci.id_estudante = %s;
    """
    update_estresse = """
        UPDATE estudante
        SET estresse = GREATEST(estresse - %s, 0)
        WHERE id_estudante = %s
        RETURNING estresse;
    """
    delete_item = """
        DELETE FROM instancia_de_item
        WHERE id_instanciaItem = %s;
    """

    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute(query_efeito, (id_instancia_item, id_estudante))
            row = cur.fetchone()
            if row is None:
                print("❌ Item não encontrado no inventário do estudante.")
                return

            efeito = row[0]

            cur.execute(update_estresse, (efeito, id_estudante))
            novo_estresse = cur.fetchone()[0]

            cur.execute(delete_item, (id_instancia_item,))

        conn.commit()
        print(f"✅ Item consumido! Estresse atual do estudante: {novo_estresse}")
        return novo_estresse

    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Erro ao consumir item: {e}")

    finally:
        if conn:
            conn.close()
