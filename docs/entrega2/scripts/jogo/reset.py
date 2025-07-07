# jogo/reset.py

import os
from .db import get_db_connection

# Comando SQL para limpar todas as tabelas
TRUNCATE_TABLES_SQL = """
TRUNCATE TABLE
    tema, tipoHabilidade, tipo_criatura, campus, setor, sala_comum,
    estudante, afinidade, dungeon_academica, tipo_item, reliquia, boss,
    monstro_simples, instancia_de_criatura, consumivel, equipavel,
    monetario, loja_item, habilidade_criatura, habilidade_estudante,
    habilidade_loja, instancia_de_item, "ataque", "cura", "defesa"
RESTART IDENTITY CASCADE;
"""

def _execute_sql_file(cur, file_path):
    """Lê e executa o conteúdo de um arquivo .sql."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            sql_script = f.read()
            cur.execute(sql_script)
            print(f"✅ Script '{os.path.basename(file_path)}' executado com sucesso.")
    except FileNotFoundError:
        print(f"❌ ERRO: Arquivo de script não encontrado em: {file_path}")
        raise
    except Exception as e:
        print(f"❌ ERRO ao executar o script '{os.path.basename(file_path)}': {e}")
        raise

def reiniciar_banco_de_dados():
    """Limpa todas as tabelas e repopula o banco de dados a partir dos scripts DML."""
    conn = None
    try:
        print("\n⏳ Iniciando a reinicialização do banco de dados...")
        conn = get_db_connection()
        cur = conn.cursor()

        # Desabilita triggers para a limpeza
        print("1/4 - Desabilitando regras de sessão...")
        cur.execute("SET session_replication_role = 'replica';")

        # Limpa as tabelas
        print("2/4 - Limpando todas as tabelas...")
        cur.execute(TRUNCATE_TABLES_SQL)
        print("✅ Tabelas limpas e contadores de ID reiniciados.")
        
        # Reabilita triggers
        print("3/4 - Reabilitando regras de sessão...")
        cur.execute("SET session_replication_role = 'origin';")

        # Repopula o banco executando o DML.sql
        print("4/4 - Repopulando o banco de dados...")
        
        # ======== CAMINHO CORRIGIDO AQUI ========
        # Sobe apenas um nível para encontrar o DML.sql na pasta 'scripts'
        dml_path = os.path.join(os.path.dirname(__file__), '..', 'DML.sql')
        _execute_sql_file(cur, os.path.normpath(dml_path))
        
        conn.commit()
        print("\n🎉 Banco de dados reiniciado com sucesso!")

    except Exception as e:
        if conn:
            conn.rollback()
        print(f"\n❌ A reinicialização falhou: {e}")
    finally:
        if conn:
            conn.close()