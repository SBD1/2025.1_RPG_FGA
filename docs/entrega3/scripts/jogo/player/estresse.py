from jogo.db import get_db_connection
import math

def verifica_estresse(jogador):

    if not jogador or "estresse" not in jogador:
        raise ValueError("Dicionário de jogador inválido ou sem chave 'estresse'.")

    
    nivel = jogador["estresse"]

    
    if nivel < 100:
        return
    penalidade_estresse(jogador)


def penalidade_estresse(jogador):
    

    if not jogador or "total_dinheiro" not in jogador or "id" not in jogador:
        raise ValueError("Dicionário de jogador inválido ou incompleto.")

    dinheiro_atual = jogador["total_dinheiro"]

    
    if dinheiro_atual == 0:
        jogador["estresse"] = 0  

        print("\n=========================")
        print("\n=========================")
        print(f"O estresse foi zerado, mas não havia dinheiro para deduzir.")
        print("\n=========================")
        print("\n=========================")
        _persistir_estudante(jogador["id"], dinheiro_atual, 0)
        return

    
    deducao = max(1, round(dinheiro_atual * 0.10))

    
    novo_total = max(0, dinheiro_atual - deducao)

    
    jogador["total_dinheiro"] = novo_total
    jogador["estresse"] = 0

    print("\n=========================")
    print("\n========= aviso =========")
    print(
        f"⚠️  Estresse excedeu o limite!\n"
        f"💸 Dinheiro antes: {dinheiro_atual}\n"
        f"💸 Dinheiro deduzido (10 %): {deducao}\n"
        f"💸 Dinheiro atual: {novo_total}\n"
        f"🧘 Estresse foi zerado."
    )
    print("\n=========================")
    print("\n=========================")

    _persistir_estudante(jogador["id"], novo_total, 0)


def _persistir_estudante(id_estudante, novo_dinheiro, novo_estresse):

    conn = get_db_connection()
    if not conn:
        print("Não foi possível conectar ao banco para salvar penalidade.")
        return

    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE estudante
                    SET total_dinheiro = %s,
                        estresse       = %s
                    WHERE id_estudante = %s
                    """,
                    (novo_dinheiro, novo_estresse, id_estudante),
                )
    except Exception as e:
        print("Erro ao aplicar penalidade no banco:", e)
    finally:
        conn.close()

def penalidade_estresse(id_estudante):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Atualiza estresse somando +10, mas limita o máximo a 100
        cur.execute("""
            UPDATE estudante
            SET estresse = LEAST(estresse + 10, 100)
            WHERE id_estudante = %s
        """, (id_estudante,))
        
        conn.commit()
        cur.close()
        conn.close()
        print("⚠️ Estresse aumentado em 10 devido à derrota.")
    except Exception as e:
        print(f"Erro ao aplicar penalidade de estresse: {e}")

def penalidade_estresse_fuga(id_estudante):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Atualiza estresse somando +5, mas limita o máximo a 100
        cur.execute("""
            UPDATE estudante
            SET estresse = LEAST(estresse + 5, 100)
            WHERE id_estudante = %s
        """, (id_estudante,))
        
        conn.commit()
        cur.close()
        conn.close()
        print("⚠️ Estresse aumentado em 5 devido à fuga.")
    except Exception as e:
        print(f"Erro ao aplicar penalidade de estresse: {e}")