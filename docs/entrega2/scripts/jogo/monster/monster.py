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

def recompensa(id_instancia_criatura: int, id_estudante: int):
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:

            # Buscar moedas, xp e id_tema com base na instância da criatura
            cur.execute("""
                SELECT
                    COALESCE(ms.qtd_moedas, 0) AS moedas,
                    COALESCE(ms.xp_tema, b.nivel * 10) AS xp,
                    da.id_tema
                FROM instancia_de_criatura ic
                LEFT JOIN monstro_simples ms ON ic.id_criatura = ms.id_criatura
                LEFT JOIN boss b ON ic.id_criatura = b.id_criatura
                JOIN dungeon_academica da ON ic.id_dungeon = da.id_dungeon
                WHERE ic.id_instanciaCriatura = %s;
            """, (id_instancia_criatura,))
            resultado = cur.fetchone()

            if resultado is None:
                raise ValueError("❌ Instância de criatura não encontrada.")

            moedas, xp, id_tema = resultado

            # Atualiza as moedas do estudante
            cur.execute("""
                UPDATE estudante
                SET total_dinheiro = total_dinheiro + %s
                WHERE id_estudante = %s;
            """, (moedas, id_estudante))

            # Verifica se o estudante já tem afinidade com o tema
            cur.execute("""
                SELECT xp_atual FROM afinidade
                WHERE id_estudante = %s AND id_tema = %s;
            """, (id_estudante, id_tema))
            afinidade = cur.fetchone()

            if afinidade:
                # Atualiza XP na afinidade existente
                cur.execute("""
                    UPDATE afinidade
                    SET xp_atual = xp_atual + %s
                    WHERE id_estudante = %s AND id_tema = %s;
                """, (xp, id_estudante, id_tema))
            else:
                # Cria afinidade se não existir
                cur.execute("""
                    INSERT INTO afinidade (id_estudante, id_tema, xp_atual, nivel_atual)
                    VALUES (%s, %s, %s, 1);
                """, (id_estudante, id_tema, xp))

            conn.commit()
            print(f"🎁 Recompensa aplicada: +{moedas} moedas, +{xp} XP em tema ID {id_tema}.")

    except Exception as e:
        print(f"⚠️ Erro ao aplicar recompensa: {e}")
    finally:
        if conn:
            conn.close()