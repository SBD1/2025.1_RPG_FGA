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
                SELECT id_sala FROM estudante 
                WHERE id_estudante = %s
            """, (id_estudante,))
            sala_atual = cur.fetchone()
            if not sala_atual:
                print("Estudante não encontrado ou sem sala atribuída.")
                return []
            sala_atual_id = sala_atual[0]
            
            # Buscar as salas vizinhas (prev e prox)
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
            
            print(f"\nSalas vizinhas da sala atual (ID {sala_atual_id}):")
            for sala in salas:
                print(f"ID: {sala[0]} | Nome: {sala[1]} | Campus: {sala[3]}\n   Descrição: {sala[2]}")
            return salas
        else:
            print("ID do estudante não informado.")
            return []

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


def mudar_setor_estudante(id_estudante):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # 1. Pegar sala atual do estudante
        cur.execute("""
            SELECT id_sala FROM estudante WHERE id_estudante = %s
        """, (id_estudante,))
        resultado = cur.fetchone()
        if not resultado:
            print("Estudante não encontrado ou sem sala atribuída.")
            return False
        sala_atual_id = resultado[0]

        # 2. Pegar setor atual da sala
        cur.execute("""
            SELECT id_setor FROM sala_comum WHERE id_sala = %s
        """, (sala_atual_id,))
        resultado = cur.fetchone()
        if not resultado:
            print("Sala atual do estudante não encontrada.")
            return False
        setor_atual_id = resultado[0]

        # 3. Buscar setores vizinhos (prev e prox) do setor atual
        cur.execute("""
            SELECT id_prevsetor, id_proxsetor FROM setor WHERE id_setor = %s
        """, (setor_atual_id,))
        resultado = cur.fetchone()
        if not resultado:
            print("Setor atual não encontrado.")
            return False
        prev_setor, prox_setor = resultado

        # 4. Montar lista de setores vizinhos (excluindo None)
        setores_vizinhos_ids = [s for s in (prev_setor, prox_setor) if s is not None]

        if not setores_vizinhos_ids:
            print("Nenhum setor vizinho encontrado para este setor.")
            return False

        # 5. Buscar detalhes desses setores vizinhos
        cur.execute("""
            SELECT id_setor, nome, descricao FROM setor WHERE id_setor = ANY(%s)
        """, (setores_vizinhos_ids,))
        setores_vizinhos = cur.fetchall()

        print("Setores vizinhos disponíveis para mudar:")
        for setor in setores_vizinhos:
            print(f"ID: {setor[0]} | Nome: {setor[1]} | Descrição: {setor[2]}")

        # 6. Usuário escolhe um setor vizinho
        novo_setor_id = int(input("Digite o ID do setor para onde deseja mover o estudante: "))

        if novo_setor_id not in setores_vizinhos_ids:
            print("Setor escolhido não é vizinho válido.")
            return False

        # 7. Buscar a primeira sala do setor escolhido (ordenada por id_sala)
        cur.execute("""
            SELECT id_sala FROM sala_comum WHERE id_setor = %s ORDER BY id_sala LIMIT 1
        """, (novo_setor_id,))
        resultado = cur.fetchone()

        if not resultado:
            print("Não há salas cadastradas nesse setor.")
            return False

        primeira_sala_id = resultado[0]

        # 8. Atualizar a sala do estudante para a primeira sala do setor escolhido
        cur.execute("""
            UPDATE estudante SET id_sala = %s WHERE id_estudante = %s
        """, (primeira_sala_id, id_estudante))
        conn.commit()

        print(f"Estudante {id_estudante} movido para a sala {primeira_sala_id} no setor {novo_setor_id} com sucesso!")

        return True

    except Exception as e:
        print("Erro ao mudar setor/sala do estudante:", e)
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
        print("1. Mover estudante para outra sala")
        print("2. Mudar setor do estudante (vai para a primeira sala do setor escolhido)")
        print("3. Sair")
        
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == "1":
            estudantes = listar_estudantes()
            if not estudantes:
                input("Pressione Enter para continuar...")
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
            estudantes = listar_estudantes()
            if not estudantes:
                input("Pressione Enter para continuar...")
                continue
                
            id_estudante = input("\nDigite o ID do estudante: ")
            if not id_estudante.isdigit():
                print("ID do estudante deve ser um número!")
                input("Pressione Enter para continuar...")  
                continue
            
            # Aqui chamamos a função que vai mostrar setores vizinhos e mover o estudante
            sucesso = mudar_setor_estudante(int(id_estudante))
            if sucesso:
                print("Setor alterado com sucesso!")
            else:
                print("Não foi possível alterar o setor.")
            
            input("Pressione Enter para continuar...")

        elif opcao == "3":
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida!")
            input("Pressione Enter para continuar...") 

if __name__ == "__main__":
    main()
