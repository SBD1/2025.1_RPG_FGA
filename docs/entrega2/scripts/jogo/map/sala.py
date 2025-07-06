from jogo.db import *
from jogo.map.dungeon import *


def listar_salas(id_estudante=None):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        if id_estudante:
            cur.execute("SELECT id_sala FROM estudante WHERE id_estudante = %s", (id_estudante,))
            sala_atual = cur.fetchone()
            if not sala_atual:
                print("Estudante não encontrado ou sem sala atribuída.")
                return []

            sala_atual_id = sala_atual[0]

            query = """
                SELECT s.id_sala, s.nome, s.descricao, c.nome as campus 
                FROM sala_comum s
                JOIN setor st ON s.id_setor = st.id_setor
                JOIN campus c ON st.id_campus = c.id_campus
                WHERE s.id_sala IN (
                    SELECT id_prevSala FROM sala_comum WHERE id_sala = %s
                    UNION
                    SELECT id_proxSala FROM sala_comum WHERE id_sala = %s
                )
                ORDER BY s.id_sala
            """
            cur.execute(query, (sala_atual_id, sala_atual_id))
            salas = cur.fetchall()

            # Aplica .strip() nos campos de texto
            salas_corrigidas = [
                (
                    sala[0],                    # id_sala
                    sala[1].strip(),            # nome
                    sala[2].strip(),            # descricao
                    sala[3].strip()             # campus
                )
                for sala in salas
            ]
            return salas_corrigidas

    except Exception as e:
        print("Erro ao listar salas:", e)
        return []

    finally:
        if cur: cur.close()
        if conn: conn.close()


def mover_estudante_para_sala(id_estudante, novo_id_sala):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT e.nome, s.nome FROM Estudante e
            JOIN Sala_Comum s ON e.id_sala = s.id_sala
            WHERE e.id_estudante = %s
        """, (id_estudante,))
        estudante = cur.fetchone()
        if not estudante:
            print("Estudante não encontrado.")
            return False

        cur.execute("SELECT nome FROM Sala_Comum WHERE id_sala = %s", (novo_id_sala,))
        nova_sala = cur.fetchone()
        if not nova_sala:
            print("Sala com esse ID não encontrada.")
            return False

        cur.execute("SELECT 1 FROM Estudante WHERE id_estudante = %s AND id_sala = %s", (id_estudante, novo_id_sala))
        if cur.fetchone():
            print("Você já está nesta sala.")
            return False

        cur.execute("UPDATE Estudante SET id_sala = %s WHERE id_estudante = %s", (novo_id_sala, id_estudante))
        conn.commit()

        print(f"Movido de '{estudante[1].strip()}' para '{nova_sala[0].strip()}' com sucesso!")
        return True

    except Exception as e:
        print("Erro ao mover estudante:", e)
        return False

    finally:
        if cur: cur.close()
        if conn: conn.close()


def explorar_sala(jogador):
    clear_screen()
    print("🔍 Explorando a sala...\n")

    if not tem_dungeon_interativo(jogador):
        print("❌ Não há dungeon nesta sala.")
        input("\nPressione Enter para continuar.")