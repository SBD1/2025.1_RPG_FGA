from jogo.db import get_db_connection, clear_screen
from jogo.player.inventario import *

TOTAL_RELIQUIAS_JOGO = 5  # total de relíquias no jogo

def mostrar_progresso_conclusao(jogador):
    clear_screen()
    print("=== PROGRESSO DE CONCLUSÃO DO JOGO ===\n")
    
    reliquias = buscar_reliquias(jogador['id'])
    qtd_reliquias = len(reliquias)
    porcentagem = int((qtd_reliquias / TOTAL_RELIQUIAS_JOGO) * 100)

    # Barra visual simples 10 blocos (cada bloco = 10%)
    blocos_preenchidos = int(porcentagem / 10)
    blocos_vazios = 10 - blocos_preenchidos
    barra = "🟩" * blocos_preenchidos + "⬛" * blocos_vazios

    print(f"Relíquias obtidas: {qtd_reliquias} / {TOTAL_RELIQUIAS_JOGO}")
    print(f"Progresso: [{barra}] {porcentagem}%\n")

    if porcentagem == 100:
        print("🎉 Parabéns! Você coletou todas as relíquias do jogo!")
        print("[1] Concluir o jogo e resetar o progresso")
        print("[2] Voltar ao menu")
        escolha = input("\nEscolha uma opção: ").strip()
        if escolha == '1':
            resetar_jogo(jogador['id'])
            print("\n✨ Jogo concluído e progresso resetado! Obrigado por jogar! ✨")
            input("\nPressione Enter para sair.")
            exit()  # encerra o programa (ou pode ajustar conforme seu fluxo)
        else:
            print("Voltando ao menu do jogador...")
            input("\nPressione Enter para continuar.")
    else:
        print("Você ainda não coletou todas as relíquias.")
        print("Volte aqui quando tiver coletado todas para concluir o jogo.")
        input("\nPressione Enter para voltar ao menu.")

def resetar_jogo(id_estudante):
    """
    Função que reseta o progresso do jogo para o jogador.
    Aqui você deve implementar as queries para limpar dados essenciais do jogador,
    como instâncias de itens, progresso, status, etc.
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        # Exemplo de reset básico:
        # Apaga todas as instâncias de itens do jogador (inclusive relíquias)
        cur.execute("DELETE FROM instancia_de_item WHERE id_estudante = %s;", (id_estudante,))

        # Reseta vida, estresse, dinheiro e sala para valores iniciais (ajuste conforme sua lógica)
        cur.execute("""
            UPDATE estudante
            SET vida = 100,
                estresse = 0,
                total_dinheiro = 0,
                id_sala = 1  -- supondo sala inicial 1
            WHERE id_estudante = %s;
        """, (id_estudante,))

        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Erro ao resetar o jogo: {e}")
