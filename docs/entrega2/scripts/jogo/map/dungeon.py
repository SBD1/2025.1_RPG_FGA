from jogo.db import get_db_connection, clear_screen
from jogo.combate.main import iniciar_combate
from jogo.player.afinidade import carregar_afinidades_estudante
from jogo.monster.boss import recompensa_boss

BOSS_POR_TEMA = {
    1: 11,  # Matemática
    2: 12,  # Programação
    3: 14,  # Engenharias
    4: 13,  # Humanidades
    5: 15   # Gerais
}

def tem_dungeon_interativo(jogador):
    id_sala = jogador['id_sala']
    id_estudante = jogador['id']

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT s.tem_dungeon, d.id_dungeon, d.nome, d.descricao, d.id_tema, t.nome
            FROM sala_comum s
            JOIN dungeon_academica d ON d.id_dungeon = s.id_sala
            JOIN tema t ON d.id_tema = t.id_tema
            WHERE s.id_sala = %s
        """, (id_sala,))
        resultado = cur.fetchone()

        if not resultado or not resultado[0]:
            print("\n📭 Esta sala não possui uma dungeon.")
            input("\nPressione Enter para voltar.")
            return False

        _, id_dungeon, nome_dungeon, descricao_dungeon, id_tema, tema_nome = resultado
        id_boss = BOSS_POR_TEMA.get(id_tema)

        boss_info = None
        possui_reliquia = False
        if id_boss:
            cur.execute("""
                SELECT b.id_criatura, b.nome, b.descricao, b.nivel, b.vida_max, b.id_reliquia, r.nome
                FROM boss b
                JOIN reliquia r ON b.id_reliquia = r.id_reliquia
                WHERE b.id_criatura = %s
            """, (id_boss,))
            boss_info = cur.fetchone()

            if boss_info:
                id_criatura_boss, nome_boss, desc_boss, nivel_boss, vida_max_boss, id_reliquia, nome_reliquia = boss_info

                cur.execute("""
                    SELECT 1
                    FROM instancia_de_item ii
                    JOIN reliquia r ON ii.id_item = r.id_reliquia
                    WHERE ii.id_estudante = %s AND r.id_reliquia = %s
                    LIMIT 1
                """, (id_estudante, id_reliquia))
                possui_reliquia = cur.fetchone() is not None

        status = "Aberta ✅" if not possui_reliquia else "Fechada ❌ (Você já possui a relíquia do boss)"

        clear_screen()
        print("="*50)
        print(f"🏰 Dungeon: {nome_dungeon.strip()}")
        print(f"📚 Tema: {tema_nome.strip()}")
        print(f"📝 Descrição: {descricao_dungeon.strip()}")
        print(f"🔐 Status: {status}")
        print("="*50)

        if possui_reliquia:
            print("\nVocê já concluiu essa dungeon.")
            input("\nPressione Enter para voltar.")
            return True

        print("\nOpções:")
        print("[1] Ver detalhes do Boss e Monstros")
        print("[2] Voltar")
        escolha = input("Escolha uma opção: ").strip()

        if escolha == '1':
            clear_screen()
            print("="*50)
            if boss_info:
                print(f"🦹 Boss: {nome_boss.strip()} (Nível {nivel_boss})")
                print(f"Descrição: {desc_boss.strip()}")
                print(f"Vida Máx: {vida_max_boss}")
                print(f"Relíquia: {nome_reliquia.strip()}")
            else:
                print("⚠️ Nenhum boss encontrado para este tema.")
            print("="*50)

            # Monstros simples da dungeon
            cur.execute("""
                SELECT ic.id_instanciaCriatura, m.id_criatura, m.nome, m.descricao, m.nivel, m.vida_max,
                       ic.vida_atual, m.qtd_moedas, m.xp_tema
                FROM instancia_de_criatura ic
                JOIN monstro_simples m ON ic.id_criatura = m.id_criatura
                WHERE ic.id_dungeon = %s
            """, (id_dungeon,))
            monstros = cur.fetchall()

            print("\n👾 Monstros Simples na Dungeon:\n")
            if not monstros:
                print("Nenhum monstro simples encontrado.")
            else:
                print(f"{'Nº':<4} {'Nome':<25} {'Nível':<6} {'Vida':<10} {'XP':<5} {'Moedas':<7}")
                print("-"*60)
                for idx, m in enumerate(monstros, start=1):
                    id_inst_criatura, id_c, nome, desc, nivel_m, vida_max_m, vida_atual, moedas, xp = m
                    vida_str = f"{vida_atual}/{vida_max_m}"
                    print(f"{idx:<4} {nome.strip():<25} {nivel_m:<6} {vida_str:<10} {xp:<5} {moedas:<7}")
                print("-"*60)

            print("\nOpções de Combate:")
            print("[1] Matar Monstro")
            print("[2] Matar BOSS")
            print("[0] Voltar")

            escolha_acao = input("Escolha uma ação: ").strip()

            if escolha_acao == '1':
                escolha_monstro = input("\nDigite o número do monstro para enfrentar: ").strip()
                if escolha_monstro.isdigit():
                    escolha_monstro = int(escolha_monstro)
                    if 1 <= escolha_monstro <= len(monstros):
                        monstro = monstros[escolha_monstro - 1]
                        id_inst_criatura = monstro[0]
                        print(f"\n⚔️ Você escolheu enfrentar {monstro[2].strip()}!")
                        input("\nPressione Enter para iniciar o combate...")

                        resultado, vida_restante = iniciar_combate(id_estudante, id_inst_criatura)

                        if resultado == 'vitoria':
                            print("🏆 Você venceu o monstro!")
                        elif resultado == 'derrota':
                            print("💀 Você foi derrotado pelo monstro!")
                        elif resultado == 'fugiu':
                            print("🏃 Você fugiu do combate!")
                        input("\nPressione Enter para continuar.")
                    else:
                        print("Opção inválida.")
                else:
                    print("Entrada inválida.")

            elif escolha_acao == '2':
                afinidades = carregar_afinidades_estudante(id_estudante)
                afinidade_tema = next((a for a in afinidades if a['id_tema'] == id_tema), None)

                if afinidade_tema and afinidade_tema['nivel'] >= 20:
                    print(f"\n⚔️ Você está pronto para enfrentar o BOSS: {nome_boss.strip()}!")
                    input("\nPressione Enter para iniciar o combate...")

                    resultado, vida_restante = iniciar_combate(id_estudante, id_boss)

                    if resultado == 'vitoria':
                        recompensa_boss(id_boss, id_estudante)
                        print("🏆 Você venceu o BOSS!")
                    elif resultado == 'derrota':
                        print("💀 Você foi derrotado pelo BOSS!")
                    elif resultado == 'fugiu':
                        print("🏃 Você fugiu do combate!")

                    input("\nPressione Enter para continuar.")
                else:
                    print("\n🔒 Você ainda não está pronto para enfrentar o boss.")
                    print("Volte quando tiver nível 20 nessa afinidade.")
                    input("\nPressione Enter para continuar.")

        else:
            print("Voltando...")

        return True

    except Exception as e:
        print(f"❌ Erro ao acessar dungeon: {e}")
        return False

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
