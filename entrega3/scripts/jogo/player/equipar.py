from jogo.db import get_db_connection

def atualizar_status_equipavel(id_instancia_item):
    query = """
    UPDATE instancia_de_item
    SET equipado = NOT equipado
    WHERE id_instanciaItem = %s;
    """
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute(query, (id_instancia_item,))  # Só o ID aqui
            conn.commit()
            print("✅ Status do item atualizado com sucesso.")
    except Exception as e:
        print(f"Erro ao atualizar status do item: {e}")
    finally:
        if conn:
            conn.close()
