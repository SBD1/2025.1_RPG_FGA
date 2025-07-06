from jogo.db import get_db_connection

def mudar_setor_estudante(id_estudante):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Sala atual
        cur.execute("SELECT id_sala FROM estudante WHERE id_estudante = %s", (id_estudante,))
        resultado = cur.fetchone()
        if not resultado:
            print("Estudante não encontrado.")
            return False
        sala_atual_id = resultado[0]

        # Setor atual
        cur.execute("SELECT id_setor FROM sala_comum WHERE id_sala = %s", (sala_atual_id,))
        resultado = cur.fetchone()
        if not resultado:
            print("Sala atual do estudante não encontrada.")
            return False
        setor_atual_id = resultado[0]

        # Setores vizinhos
        cur.execute("SELECT id_prevsetor, id_proxsetor FROM setor WHERE id_setor = %s", (setor_atual_id,))
        resultado = cur.fetchone()
        if not resultado:
            print("Setor atual não encontrado.")
            return False
        prev_setor, prox_setor = resultado
        setores_vizinhos_ids = [s for s in (prev_setor, prox_setor) if s is not None]

        if not setores_vizinhos_ids:
            print("Nenhum setor vizinho disponível.")
            return False

        # Detalhes dos setores vizinhos
        cur.execute("SELECT id_setor, nome, descricao FROM setor WHERE id_setor = ANY(%s)", (setores_vizinhos_ids,))
        setores_vizinhos = cur.fetchall()

        print("\nSetores vizinhos disponíveis:")
        for setor in setores_vizinhos:
            print(f"ID: {setor[0]} | Nome: {setor[1]}\nDescrição: {setor[2]}")

        # Escolha do setor
        novo_setor_id = int(input("\nDigite o ID do setor para onde deseja ir: "))
        if novo_setor_id not in setores_vizinhos_ids:
            print("Setor inválido.")
            return False

        # Primeira sala do setor escolhido
        cur.execute("SELECT id_sala, nome FROM sala_comum WHERE id_setor = %s ORDER BY id_sala LIMIT 1", (novo_setor_id,))
        resultado = cur.fetchone()
        if not resultado:
            print("Nenhuma sala disponível nesse setor.")
            return False

        nova_sala_id, nova_sala_nome = resultado

        # Atualiza estudante
        cur.execute("UPDATE estudante SET id_sala = %s, estresse = estresse + 1 WHERE id_estudante = %s", (nova_sala_id, id_estudante))
        conn.commit()

        print(f"\n✅ Estudante movido para a sala '{nova_sala_nome.strip()}' no setor {novo_setor_id}.")
        return nova_sala_nome  # retorna nome da nova sala

    except Exception as e:
        print("Erro ao mudar de setor:", e)
        return False

    finally:
        if cur: cur.close()
        if conn: conn.close()