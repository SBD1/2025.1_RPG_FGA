import psycopg2
import os

def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname="rpg_fga",
            user="estudante",
            password="123",
            host="localhost",
            port="5432"
        )
        return conn
    except Exception as e:
        print("❌ Erro ao conectar ao banco de dados:", e)
        return None


def clear_screen():
    """Limpa o terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')
