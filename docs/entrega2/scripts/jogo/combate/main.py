# ===== main.py =====
import psycopg2
from jogo.combate.inteligencia import escolher_acao_monstro
from jogo.combate.regras import aplicar_regras
from jogo.combate.combate import menu, escolher_habilidade, atualizar_cooldowns
import os
import sys
from jogo.db import *

def limpar_tela():
    try:
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
    except:
        print('\n' * 100)
    if sys.stdout.isatty():
        print("\033[H\033[J", end='')

def carregar_habilidades_jogador(conn, id_jogador):
    habilidades = {'ataque': {}, 'defesa': {}, 'cura': {}}
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT he.id_habilidade,
                       th.tipo_habilidade,
                       COALESCE(a.nome, c.nome, d.nome) AS nome,
                       COALESCE(a.nivel, c.nivel, d.nivel) AS nivel,
                       COALESCE(a.coolDown, c.coolDown, d.coolDown) AS cooldown,
                       a.danoCausado,
                       c.vidaRecuperada,
                       d.danoMitigado,
                       t.nome AS tema
                FROM habilidade_estudante he
                JOIN tipoHabilidade th ON he.id_habilidade = th.id_habilidade
                LEFT JOIN Ataque a ON he.id_habilidade = a.id_habilidade
                LEFT JOIN Cura c ON he.id_habilidade = c.id_habilidade
                LEFT JOIN Defesa d ON he.id_habilidade = d.id_habilidade
                JOIN tema t ON COALESCE(a.id_tema, c.id_tema, d.id_tema) = t.id_tema
                WHERE he.id_estudante = %s
            """, (id_jogador,))
            for row in cur.fetchall():
                tipo_habilidade = row[1].lower().strip()
                nome = row[2].strip() if row[2] else None
                cooldown = row[4] or 0
                if tipo_habilidade == 'ataque':
                    potencia = row[5] or 0
                elif tipo_habilidade == 'cura':
                    potencia = row[6] or 0
                elif tipo_habilidade == 'defesa':
                    potencia = row[7] or 0
                else:
                    continue
                tema = row[8][0].upper() if row[8] else 'G'
                habilidades[tipo_habilidade][nome] = {
                    'tipo': tema,
                    'potencia': potencia,
                    'cooldown': cooldown
                }
    except psycopg2.Error as e:
        print(f"Erro ao carregar habilidades do jogador: {e}")
        return None
    return habilidades

def carregar_habilidades_monstro(conn, id_monstro):
    habilidades = {'ataque': {}, 'defesa': {}, 'cura': {}}
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT hc.id_habilidade,
                       th.tipo_habilidade,
                       COALESCE(a.nome, c.nome, d.nome) AS nome,
                       COALESCE(a.nivel, c.nivel, d.nivel) AS nivel,
                       COALESCE(a.coolDown, c.coolDown, d.coolDown) AS cooldown,
                       a.danoCausado,
                       c.vidaRecuperada,
                       d.danoMitigado,
                       t.nome AS tema
                FROM habilidade_criatura hc
                JOIN tipoHabilidade th ON hc.id_habilidade = th.id_habilidade
                LEFT JOIN Ataque a ON hc.id_habilidade = a.id_habilidade
                LEFT JOIN Cura c ON hc.id_habilidade = c.id_habilidade
                LEFT JOIN Defesa d ON hc.id_habilidade = d.id_habilidade
                JOIN tema t ON COALESCE(a.id_tema, c.id_tema, d.id_tema) = t.id_tema
                WHERE hc.id_criatura = %s
            """, (id_monstro,))
            for row in cur.fetchall():
                tipo_habilidade = row[1].lower().strip()
                nome = row[2].strip() if row[2] else None
                cooldown = row[4] or 0
                if tipo_habilidade == 'ataque':
                    potencia = row[5] or 0
                elif tipo_habilidade == 'cura':
                    potencia = row[6] or 0
                elif tipo_habilidade == 'defesa':
                    potencia = row[7] or 0
                else:
                    continue
                tema = row[8][0].upper() if row[8] else 'G'
                habilidades[tipo_habilidade][nome] = {
                    'tipo': tema,
                    'potencia': potencia,
                    'cooldown': cooldown
                }
    except psycopg2.Error as e:
        print(f"Erro ao carregar habilidades do monstro: {e}")
        return None
    return habilidades

def carregar_vida_jogador(conn, id_jogador):
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT vida FROM estudante WHERE id_estudante = %s", (id_jogador,))
            result = cur.fetchone()
            return result[0] if result else 200
    except psycopg2.Error as e:
        print(f"Erro ao carregar vida do jogador: {e}")
        return 200

def carregar_vida_monstro(conn, id_monstro):
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT vida_max FROM monstro_simples WHERE id_criatura = %s
                UNION
                SELECT vida_max FROM boss WHERE id_criatura = %s
            """, (id_monstro, id_monstro))
            result = cur.fetchone()
            return result[0] if result else 200
    except psycopg2.Error as e:
        print(f"Erro ao carregar vida do monstro: {e}")
        return 200

def iniciar_combate(id_jogador, id_monstro):
    conn = None
    try:
        conn = get_db_connection()
        habilidades_jogador = carregar_habilidades_jogador(conn, id_jogador)
        habilidades_monstro = carregar_habilidades_monstro(conn, id_monstro)
        if habilidades_jogador is None or habilidades_monstro is None:
            return "erro", 0

        vida_max_jogador = carregar_vida_jogador(conn, id_jogador)
        vida_max_monstro = carregar_vida_monstro(conn, id_monstro)
        vida_jogador = vida_max_jogador
        vida_monstro = vida_max_monstro

        cooldowns_jogador = {}
        cooldowns_monstro = {}

        categoria_map = {'A': 'ataque', 'D': 'defesa', 'C': 'cura', 'P': 'passar'}
        fugiu = False

        while vida_jogador > 0 and vida_monstro > 0:
            limpar_tela()
            menu(vida_jogador, vida_monstro, vida_max_jogador, vida_max_monstro)
            entrada = input("Digite sua escolha: ").upper()

            if entrada == 'F':
                print("🏃 Você fugiu do combate!")
                fugiu = True
                break

            if entrada not in categoria_map:
                print("Opção inválida. Escolha A, D, C, P ou F.")
                continue

            j_categoria = categoria_map[entrada]
            j_nome, j_habilidade = (None, None)
            if j_categoria != 'passar':
                j_nome, j_habilidade = escolher_habilidade(
                    j_categoria, habilidades_jogador, cooldowns_jogador, vida_jogador, vida_monstro
                )
                if j_nome is None:
                    continue
            else:
                j_nome = 'Nenhuma ação'
                j_habilidade = {'tipo': 'G', 'potencia': 0, 'cooldown': 0}

            m_categoria, resultado = escolher_acao_monstro(
                habilidades_monstro, vida_monstro, vida_jogador, cooldowns_monstro, j_categoria, j_habilidade['tipo']
            )
            m_nome, m_habilidade = resultado

            if m_nome is None:
                m_categoria = 'passar'
                m_nome = 'Nenhuma ação'
                m_habilidade = {'tipo': 'G', 'potencia': 0, 'cooldown': 0}

            vida_jogador, vida_monstro = aplicar_regras(
                j_categoria, j_nome, j_habilidade,
                m_categoria, m_nome, m_habilidade,
                vida_jogador, vida_monstro,
                vida_max_jogador, vida_max_monstro
            )

            if j_categoria != 'passar':
                cooldowns_jogador[j_nome] = j_habilidade.get('cooldown', 0)
            if m_categoria != 'passar':
                cooldowns_monstro[m_nome] = m_habilidade.get('cooldown', 0)

            atualizar_cooldowns(cooldowns_jogador)
            atualizar_cooldowns(cooldowns_monstro)

        if not fugiu:
            print("\n=========== RESULTADO FINAL ===========")
            if vida_jogador <= 0 and vida_monstro <= 0:
                print("⚔️ Empate! Ambos caíram no campo de batalha!")
                return "empate", vida_jogador
            elif vida_jogador <= 0:
                print("💀 Você foi derrotado pelo monstro!")
                return "derrota", vida_jogador
            elif vida_monstro <= 0:
                print("🏆 Vitória! Você derrotou o monstro!")
                return "vitoria", vida_jogador
        else:
            return "fuga", vida_jogador

    except psycopg2.Error as e:
        print(f"❌ Erro ao conectar ao banco de dados: {e}")
        return "erro", 0
    except Exception as e:
        print(f"❌ Erro durante o combate: {e}")
        return "erro", 0
    finally:
        if conn:
            conn.close()
