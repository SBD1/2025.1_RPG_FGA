from jogo.db import get_db_connection

def listar_salas_com_dungeon():
    try:
        conn = get_db_connection()
        if not conn:
            print("Falha ao conectar ao banco de dados.")
            return

        cur = conn.cursor()
        query = """
            SELECT s.id_sala, s.nome AS nome_sala, d.nome AS nome_dungeon, d.descricao
            FROM sala_comum s
            JOIN dungeon_academica d ON s.id_sala = d.id_dungeon
            ORDER BY s.id_sala;
        """
        cur.execute(query)
        resultados = cur.fetchall()

        print(f"Quantidade de registros encontrados: {len(resultados)}")

        if resultados:
            print("Salas com Dungeon Acadêmica:")
            for sala_id, nome_sala, nome_dungeon, descricao in resultados:
                print(f"ID Sala: {sala_id} | Sala: {nome_sala.strip()} | Dungeon: {nome_dungeon.strip()} | Descrição: {descricao.strip()}")
        else:
            print("Nenhuma sala com dungeon encontrada.")

    except Exception as e:
        print("Erro ao listar salas com dungeon:", e)
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    print("Iniciando listagem de salas com dungeon...")
    listar_salas_com_dungeon()
    print("Fim do script.")
