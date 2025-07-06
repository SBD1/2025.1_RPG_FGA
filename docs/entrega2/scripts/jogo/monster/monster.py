from jogo.db import get_db_connection, clear_screen

def buscar_habilidades_criatura(id_criatura):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        query = """
        SELECT
            hc.id_habilidade,
            th.tipo_habilidade,
            COALESCE(a.nome, c.nome, d.nome) AS nome,
            COALESCE(a.nivel, c.nivel, d.nivel) AS nivel,
            COALESCE(a.coolDown, c.coolDown, d.coolDown) AS cooldown,
            a.danoCausado,
            c.vidaRecuperada,
            d.danoMitigado,
            COALESCE(a.id_tema, c.id_tema, d.id_tema) AS id_tema
        FROM habilidade_criatura hc
        JOIN tipoHabilidade th ON hc.id_habilidade = th.id_habilidade
        LEFT JOIN Ataque a ON hc.id_habilidade = a.id_habilidade
        LEFT JOIN Cura c ON hc.id_habilidade = c.id_habilidade
        LEFT JOIN Defesa d ON hc.id_habilidade = d.id_habilidade
        WHERE hc.id_criatura = %s
        """
        cur.execute(query, (id_criatura,))
        rows = cur.fetchall()

        habilidades = []
        for row in rows:
            nome_habilidade = row[2].strip() if row[2] else ''
            tipo = row[1].strip().lower() if row[1] else ''
            # define potência conforme tipo
            if tipo == 'ataque':
                potencia = row[5]
            elif tipo == 'cura':
                potencia = row[6]
            elif tipo == 'defesa':
                potencia = row[7]
            else:
                potencia = None

            habilidades.append({
                'id_habilidade': row[0],
                'tipo_habilidade': tipo,
                'nome': nome_habilidade,
                'nivel': row[3],
                'cooldown': row[4],
                'potencia': potencia,
                'id_tema': row[8]
            })
        return habilidades

    except Exception as e:
        print("Erro ao buscar habilidades da criatura:", e)
        return []
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
