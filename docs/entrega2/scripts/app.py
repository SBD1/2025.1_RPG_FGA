import psycopg2
import os

def clear_screen():
    """Limpa o terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_db_connection():
    """Função para centralizar a conexão com o banco"""
    return psycopg2.connect(
        dbname="rpg_fga",
        user="estudante",
        password="123",
        host="localhost",
        port="5432"
    )


def listar_estudantes():
    clear_screen() 
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT e.id_estudante, e.nome, s.nome as sala 
            FROM Estudante e
            JOIN Sala_Comum s ON e.id_sala = s.id_sala
            ORDER BY e.id_estudante
        """)
        estudantes = cur.fetchall()

        print("\nEstudantes disponíveis:")
        for estudante in estudantes:
            print(f"ID: {estudante[0]} | Nome: {estudante[1]} | Sala atual: {estudante[2]}")
        return estudantes
    
    except Exception as e:
        print("Erro ao listar estudantes:", e)
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def listar_salas(id_estudante=None):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        if id_estudante:
            # Obter a sala atual do estudante
            cur.execute("""
                SELECT id_sala FROM Estudante 
                WHERE id_estudante = %s
            """, (id_estudante,))
            sala_atual = cur.fetchone()
            sala_atual_id = sala_atual[0] if sala_atual else None
        else:
            sala_atual_id = None

        # Consulta principal com filtro para excluir a sala atual se houver estudante
        query = """
            SELECT s.id_sala, s.nome, s.descricao, c.nome as campus 
            FROM Sala_Comum s
            JOIN Setor st ON s.id_setor = st.id_setor
            JOIN Campus c ON st.id_campus = c.id_campus
            %s
            ORDER BY s.id_sala
        """ % ("WHERE s.id_sala != %s" if sala_atual_id else "")
        
        params = (sala_atual_id,) if sala_atual_id else ()
        
        cur.execute(query, params)
        salas = cur.fetchall()
        
        print("\nSalas disponíveis:" + (f" (exceto sala atual)" if sala_atual_id else ""))
        for sala in salas:
            print(f"ID: {sala[0]} | Nome: {sala[1]} | Campus: {sala[3]}\n   Descrição: {sala[2]}")
        return salas
        
    except Exception as e:
        print("Erro ao listar salas:", e)
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def mover_estudante_para_sala(id_estudante, novo_id_sala):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Verificar se o estudante existe
        cur.execute("""
            SELECT e.nome, s.nome as sala_atual 
            FROM Estudante e
            JOIN Sala_Comum s ON e.id_sala = s.id_sala
            WHERE e.id_estudante = %s
        """, (id_estudante,))
        estudante = cur.fetchone()
        
        if not estudante:
            print(f"\n❌ Estudante com ID '{id_estudante}' não encontrado.")
            return False

        # Verificar se a nova sala existe
        cur.execute("""
            SELECT nome FROM Sala_Comum 
            WHERE id_sala = %s
        """, (novo_id_sala,))
        nova_sala = cur.fetchone()
        
        if not nova_sala:
            print(f"\n❌ Sala com ID '{novo_id_sala}' não encontrada.")
            return False

        # Verificar se já está na sala
        cur.execute("""
            SELECT 1 FROM Estudante 
            WHERE id_estudante = %s AND id_sala = %s
        """, (id_estudante, novo_id_sala))
        if cur.fetchone():
            print(f"\nℹ️ O estudante '{estudante[0]}' já está na sala '{nova_sala[0]}'")
            return False

        # Atualizar sala
        cur.execute("""
            UPDATE Estudante 
            SET id_sala = %s 
            WHERE id_estudante = %s
        """, (novo_id_sala, id_estudante))
        conn.commit()
        
        print(f"\n✅ Estudante '{estudante[0]}' movido da sala '{estudante[1]}' para '{nova_sala[0]}' com sucesso!")
        return True

    except Exception as e:
        print("\n❌ Erro ao mover estudante:", e)
        return False
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def main():
    while True:
        clear_screen() 
        print("\n=== Sistema de Movimentação de Estudantes ===")
        print("\nOpções:")
        print("1. Mover estudante")
        print("2. Sair")
        
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == "1":
            estudantes = listar_estudantes()
            if not estudantes:
                continue
                
            id_estudante = input("\nDigite o ID do estudante: ")
            if not id_estudante.isdigit():
                print("ID do estudante deve ser um número!")
                input("Pressione Enter para continuar...")  
                continue
                
            listar_salas(int(id_estudante))
            novo_id_sala = input("\nDigite o ID da nova sala: ")
            if not novo_id_sala.isdigit():
                print("ID da sala deve ser um número!")
                input("Pressione Enter para continuar...") 
                continue
                
            mover_estudante_para_sala(int(id_estudante), int(novo_id_sala))
            input("Pressione Enter para continuar...")  
        elif opcao == "2":
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida!")
            input("Pressione Enter para continuar...") 

if __name__ == "__main__":
    main()