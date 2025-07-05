from jogo.db import get_db_connection


def buscar_habilidades_estudante_todas(id_estudante):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        query = """
        SELECT
            he.id_habilidade,
            th.tipo_habilidade,
            COALESCE(a.nome, c.nome, d.nome) AS nome,
            COALESCE(a.nivel, c.nivel, d.nivel) AS nivel,
            COALESCE(a.coolDown, c.coolDown, d.coolDown) AS cooldown,
            a.danoCausado,
            c.vidaRecuperada,
            d.danoMitigado,
            tm.nome AS nome_tema
        FROM habilidade_estudante he
        JOIN tipoHabilidade th ON he.id_habilidade = th.id_habilidade
        LEFT JOIN Ataque a ON he.id_habilidade = a.id_habilidade
        LEFT JOIN Cura c ON he.id_habilidade = c.id_habilidade
        LEFT JOIN Defesa d ON he.id_habilidade = d.id_habilidade
        LEFT JOIN tema tm ON COALESCE(a.id_tema, c.id_tema, d.id_tema) = tm.id_tema
        WHERE he.id_estudante = %s;
        """
        cur.execute(query, (id_estudante,))
        rows = cur.fetchall()
        
        habilidades = []
        for row in rows:
            nome_habilidade = row[2].strip() if row[2] else ''
            tipo = row[1].strip().lower() if row[1] else ''
            nome_tema = row[8].strip() if row[8] else 'N/A'
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
                'nome_tema': nome_tema
            })
        return habilidades
        
    except Exception as e:
        print("Erro ao buscar habilidades:", e)
        return []
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def mostrar_catalogo_habilidades(habilidades):
    if not habilidades:
        print("\n❌ Nenhuma habilidade encontrada.")
        return

    print("\n" + "=" * 120)
    print("🧠 CATÁLOGO DE HABILIDADES 🧠".center(120))
    print("=" * 120)
    
    for h in habilidades:
        potencia_str = str(h['potencia']) if h['potencia'] is not None else '-'
        print(f"ID: {h['id_habilidade']:>3} | "
              f"Nome: {h['nome']:<20} | "
              f"Tipo: {h['tipo_habilidade']:<7} | "
              f"Nível: {h['nivel']:<2} | "
              f"CD: {h['cooldown']:<2} | "
              f"Potência: {potencia_str:<3} | "
              f"Tema: {h['nome_tema']}")
    
    print("=" * 120)