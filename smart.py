import sys
import mysql.connector
from datetime import date

try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

# ---------------- CONEXÃO ---------------- #

try:
    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="smart_stock"
    )
    cursor = conexao.cursor()
    print("✅ Conectado ao banco de dados com sucesso!")
except mysql.connector.Error as e:
    print(f"❌ Erro ao conectar ao banco de dados: {e}")
    exit()


# ================================================
#               FUNÇÕES - PRODUTOS
# ================================================

def adicionar_produto():
    print("\n--- Adicionar Produto ---")
    try:
        nome = input("Digite o nome do produto: ").strip()
        if not nome:
            print("❌ O nome do produto não pode ser vazio.")
            return
        descricao = input("Digite a descrição do produto: ")
        preco = float(input("Digite o preço: R$ "))
        categoria = input("Digite a categoria: ")
        quantidade_atual = int(input("Digite a quantidade inicial em estoque: "))
        quantidade_minima = int(input("Digite a quantidade mínima em estoque (alerta): "))
        
        data_validade = None
        numero_lote = "LOTE-INICIAL"
        if quantidade_atual > 0:
            validade_str = input("Data de validade do lote inicial (AAAA-MM-DD) ou deixe em branco se não houver: ").strip()
            data_validade = validade_str if validade_str else None
            lote_str = input("Nome/Número do lote inicial (ou Enter para 'LOTE-INICIAL'): ").strip()
            if lote_str:
                numero_lote = lote_str
    except ValueError:
        print("❌ Entrada inválida! Certifique-se de digitar números válidos para preço e estoque.")
        return

    try:
        sql_produto = """
            INSERT INTO tbl_produtos (nome_produto, descricao_produto, preco_produto, categoria_produto)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql_produto, (nome, descricao, preco, categoria))
        id_produto = cursor.lastrowid

        sql_estoque = """
            INSERT INTO tbl_estoque (id_produto, quantidade_atual, quantidade_minima)
            VALUES (%s, %s, %s)
        """
        cursor.execute(sql_estoque, (id_produto, quantidade_atual, quantidade_minima))

        if quantidade_atual > 0:
            sql_lote = """
                INSERT INTO tbl_lotes (id_produto, numero_lote, quantidade_lote, data_validade, data_entrada)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql_lote, (id_produto, numero_lote, quantidade_atual, data_validade, date.today()))

        conexao.commit()
        print(f"✅ Produto '{nome}' adicionado com sucesso! (ID: {id_produto})")
    except Exception as e:
        conexao.rollback()
        print(f"❌ Erro ao adicionar produto: {e}")


def listar_produtos():
    print("\n--- Lista de Produtos ---")
    try:
        sql = """
            SELECT p.id_produtos, p.nome_produto, p.categoria_produto, p.preco_produto,
                   e.quantidade_atual, e.quantidade_minima,
                   (SELECT MIN(l.data_validade) FROM tbl_lotes l WHERE l.id_produto = p.id_produtos AND l.quantidade_lote > 0) AS proxima_validade
            FROM tbl_produtos p
            LEFT JOIN tbl_estoque e ON p.id_produtos = e.id_produto
            ORDER BY p.id_produtos
        """
        cursor.execute(sql)
        produtos = cursor.fetchall()

        if not produtos:
            print("Nenhum produto cadastrado.")
            return

        print(f"\n{'ID':<5} {'Nome':<25} {'Categoria':<20} {'Preço':>10} {'Qtd Atual':>10} {'Qtd Mín':>8} {'Próx Venc':<12} {'Status'}")
        print("-" * 105)
        for p in produtos:
            id_p, nome, cat, preco, qtd_atual, qtd_min, validade = p
            qtd_atual = qtd_atual if qtd_atual is not None else 0
            qtd_min = qtd_min if qtd_min is not None else 0
            validade_str = str(validade) if validade else "N/A"
            status = "⚠️ ESTOQUE BAIXO" if qtd_atual <= qtd_min else "✅ OK"
            print(f"{id_p:<5} {nome:<25} {cat:<20} R${preco:>8.2f} {qtd_atual:>10} {qtd_min:>8} {validade_str:<12} {status}")
    except Exception as e:
        print(f"❌ Erro ao listar produtos: {e}")


def atualizar_produto():
    print("\n--- Atualizar Produto ---")
    listar_produtos()
    try:
        id_produto = int(input("\nDigite o ID do produto que deseja atualizar: "))

        nome = input("Novo nome (deixe em branco para manter): ")
        descricao = input("Nova descrição (deixe em branco para manter): ")
        preco_str = input("Novo preço (deixe em branco para manter): ")
        categoria = input("Nova categoria (deixe em branco para manter): ")

        # Busca valores atuais
        cursor.execute("SELECT nome_produto, descricao_produto, preco_produto, categoria_produto FROM tbl_produtos WHERE id_produtos = %s", (id_produto,))
        atual = cursor.fetchone()
        if not atual:
            print("❌ Produto não encontrado.")
            return

        nome = nome if nome else atual[0]
        descricao = descricao if descricao else atual[1]
        preco = float(preco_str) if preco_str else atual[2]
        categoria = categoria if categoria else atual[3]

        sql = """
            UPDATE tbl_produtos
            SET nome_produto = %s, descricao_produto = %s, preco_produto = %s, categoria_produto = %s
            WHERE id_produtos = %s
        """
        cursor.execute(sql, (nome, descricao, preco, categoria, id_produto))
        conexao.commit()

        if cursor.rowcount > 0:
            print("✅ Produto atualizado com sucesso!")
        else:
            print("❌ Produto não encontrado.")
    except ValueError:
        print("❌ Valor inválido digitado.")
    except Exception as e:
        print(f"❌ Erro ao atualizar produto: {e}")


def excluir_produto():
    print("\n--- Excluir Produto ---")
    listar_produtos()
    try:
        id_produto = int(input("\nDigite o ID do produto que deseja excluir: "))
        confirmacao = input(f"Tem certeza que deseja excluir o produto ID {id_produto}? (s/n): ")
        if confirmacao.lower() != "s":
            print("Operação cancelada.")
            return

        # Remove estoque vinculado e itens de venda antes de remover produto
        cursor.execute("DELETE FROM tbl_item_venda WHERE id_produto = %s", (id_produto,))
        cursor.execute("DELETE FROM tbl_estoque WHERE id_produto = %s", (id_produto,))
        cursor.execute("DELETE FROM tbl_produtos WHERE id_produtos = %s", (id_produto,))
        conexao.commit()

        if cursor.rowcount > 0:
            print("✅ Produto excluído com sucesso!")
        else:
            print("❌ Produto não encontrado.")
    except ValueError:
        print("❌ ID inválido.")
    except Exception as e:
        conexao.rollback()
        print(f"❌ Erro ao excluir produto: {e}")


# ================================================
#               FUNÇÕES - ESTOQUE
# ================================================

def deduzir_estoque_lotes(id_produto, quantidade_a_deduzir):
    # Busca lotes ativos com quantidade > 0 do produto, ordenando por data_validade ASC (nulos por último), data_entrada ASC
    sql = """
        SELECT id_lote, quantidade_lote, numero_lote, data_validade
        FROM tbl_lotes
        WHERE id_produto = %s AND quantidade_lote > 0
        ORDER BY (data_validade IS NULL) ASC, data_validade ASC, data_entrada ASC
    """
    cursor.execute(sql, (id_produto,))
    lotes = cursor.fetchall()

    restante = quantidade_a_deduzir
    for id_lote, qtd_lote, num_lote, validade in lotes:
        if restante <= 0:
            break

        if qtd_lote >= restante:
            cursor.execute("UPDATE tbl_lotes SET quantidade_lote = quantidade_lote - %s WHERE id_lote = %s", (restante, id_lote))
            print(f"   Dedução no lote '{num_lote}': -{restante} unidades.")
            restante = 0
        else:
            cursor.execute("UPDATE tbl_lotes SET quantidade_lote = 0 WHERE id_lote = %s", (id_lote,))
            print(f"   Lote '{num_lote}' consumido por completo (-{qtd_lote} unidades).")
            restante -= qtd_lote

    if restante > 0:
        raise Exception(f"Erro de inconsistência no estoque por lotes! Restaram {restante} unidades sem lote correspondente.")


def atualizar_estoque():
    print("\n--- Atualizar Estoque ---")
    listar_produtos()
    try:
        id_produto = int(input("\nDigite o ID do produto: "))

        # Verifica se o produto existe no estoque
        cursor.execute("SELECT quantidade_atual FROM tbl_estoque WHERE id_produto = %s", (id_produto,))
        row = cursor.fetchone()
        if not row:
            print("❌ Produto não encontrado no estoque.")
            return
        qtd_atual = row[0]

        print("1 - Adicionar ao estoque (entrada)")
        print("2 - Remover do estoque (saída)")
        tipo = input("Escolha o tipo: ")

        quantidade = int(input("Quantidade: "))
        if quantidade <= 0:
            print("❌ Quantidade deve ser maior que zero.")
            return

        if tipo == "1":
            lote_str = input("Número/Código do lote: ").strip()
            numero_lote = lote_str if lote_str else f"LOTE-{date.today().strftime('%Y%m%d')}"
            validade_str = input("Data de validade do lote (AAAA-MM-DD) ou deixe em branco se não houver: ").strip()
            data_validade = validade_str if validade_str else None

            # Insere o novo lote
            sql_lote = """
                INSERT INTO tbl_lotes (id_produto, numero_lote, quantidade_lote, data_validade, data_entrada)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql_lote, (id_produto, numero_lote, quantidade, data_validade, date.today()))

            # Atualiza consolidado
            sql_estoque = "UPDATE tbl_estoque SET quantidade_atual = quantidade_atual + %s WHERE id_produto = %s"
            cursor.execute(sql_estoque, (quantidade, id_produto))
            conexao.commit()
            print(f"✅ Entrada registrada com sucesso no lote '{numero_lote}'!")

        elif tipo == "2":
            if qtd_atual < quantidade:
                print(f"❌ Estoque insuficiente! Disponível: {qtd_atual}")
                return

            # Deduz dos lotes
            deduzir_estoque_lotes(id_produto, quantidade)

            # Atualiza consolidado
            sql_estoque = "UPDATE tbl_estoque SET quantidade_atual = quantidade_atual - %s WHERE id_produto = %s"
            cursor.execute(sql_estoque, (quantidade, id_produto))
            conexao.commit()
            print("✅ Saída de estoque concluída com sucesso!")
        else:
            print("❌ Opção inválida.")
            return

    except ValueError:
        print("❌ Valor inválido.")
    except Exception as e:
        conexao.rollback()
        print(f"❌ Erro ao atualizar estoque: {e}")


def verificar_estoque_baixo():
    print("\n--- ⚠️  Produtos com Estoque Baixo ---")
    try:
        sql = """
            SELECT p.id_produtos, p.nome_produto, p.categoria_produto,
                   e.quantidade_atual, e.quantidade_minima
            FROM tbl_produtos p
            JOIN tbl_estoque e ON p.id_produtos = e.id_produto
            WHERE e.quantidade_atual <= e.quantidade_minima
            ORDER BY e.quantidade_atual ASC
        """
        cursor.execute(sql)
        produtos = cursor.fetchall()

        if not produtos:
            print("✅ Nenhum produto com estoque baixo!")
            return

        print(f"\n{'ID':<5} {'Nome':<25} {'Categoria':<20} {'Qtd Atual':>10} {'Qtd Mín':>8}")
        print("-" * 75)
        for p in produtos:
            print(f"{p[0]:<5} {p[1]:<25} {p[2]:<20} {p[3]:>10} {p[4]:>8}")
    except Exception as e:
        print(f"❌ Erro: {e}")


def listar_lotes_produto():
    print("\n--- Listar Lotes de um Produto ---")
    listar_produtos()
    try:
        id_produto = int(input("\nDigite o ID do produto para ver os lotes: "))

        # Verifica se o produto existe
        cursor.execute("SELECT nome_produto FROM tbl_produtos WHERE id_produtos = %s", (id_produto,))
        produto = cursor.fetchone()
        if not produto:
            print("❌ Produto não encontrado.")
            return

        cursor.execute("""
            SELECT id_lote, numero_lote, quantidade_lote, data_validade, data_entrada
            FROM tbl_lotes
            WHERE id_produto = %s AND quantidade_lote > 0
            ORDER BY data_validade ASC, data_entrada ASC
        """, (id_produto,))
        lotes = cursor.fetchall()

        print(f"\n📦 Lotes ativos para o produto: '{produto[0]}' (ID: {id_produto})")
        if not lotes:
            print("Nenhum lote ativo encontrado para este produto.")
            return

        print(f"\n{'ID Lote':<8} {'Número Lote':<20} {'Qtd Disponível':>15} {'Validade':<12} {'Data Entrada'}")
        print("-" * 72)
        for l in lotes:
            validade_str = str(l[3]) if l[3] else "N/A"
            print(f"{l[0]:<8} {l[1]:<20} {l[2]:>15} {validade_str:<12} {str(l[4])}")
    except ValueError:
        print("❌ ID inválido.")
    except Exception as e:
        print(f"❌ Erro ao listar lotes: {e}")


# ================================================
#               FUNÇÕES - VENDAS
# ================================================

def registrar_venda():
    print("\n--- Registrar Nova Venda ---")
    listar_produtos()

    itens = []
    valor_total = 0.0

    while True:
        try:
            id_produto = int(input("\nDigite o ID do produto (ou 0 para finalizar): "))
            if id_produto == 0:
                break

            cursor.execute("""
                SELECT p.nome_produto, p.preco_produto, e.quantidade_atual
                FROM tbl_produtos p
                JOIN tbl_estoque e ON p.id_produtos = e.id_produto
                WHERE p.id_produtos = %s
            """, (id_produto,))
            produto = cursor.fetchone()

            if not produto:
                print("❌ Produto não encontrado.")
                continue

            nome, preco, qtd_disponivel = produto
            print(f"Produto: {nome} | Preço: R${preco:.2f} | Disponível: {qtd_disponivel}")

            quantidade = int(input("Quantidade: "))
            if quantidade <= 0:
                print("❌ Quantidade inválida.")
                continue
            if quantidade > qtd_disponivel:
                print(f"❌ Estoque insuficiente! Disponível: {qtd_disponivel}")
                continue

            itens.append((id_produto, quantidade, float(preco)))
            valor_total += float(preco) * quantidade
            print(f"✅ Item adicionado. Subtotal: R${float(preco) * quantidade:.2f}")
        except ValueError:
            print("❌ Valor inválido.")
            continue

    if not itens:
        print("Nenhum item na venda. Operação cancelada.")
        return

    print(f"\n💰 Valor total da venda: R${valor_total:.2f}")
    confirmar = input("Confirmar venda? (s/n): ")
    if confirmar.lower() != "s":
        print("Venda cancelada.")
        return

    try:
        hoje = date.today()
        cursor.execute(
            "INSERT INTO tbl_venda (data_venda, valor_total_venda) VALUES (%s, %s)",
            (hoje, valor_total)
        )
        id_venda = cursor.lastrowid

        for id_produto, quantidade, preco_unit in itens:
            cursor.execute(
                "INSERT INTO tbl_item_venda (id_venda, id_produto, quantidade_itens, preco_unitario) VALUES (%s, %s, %s, %s)",
                (id_venda, id_produto, quantidade, preco_unit)
            )
            # Deduz a quantidade dos lotes usando FEFO
            deduzir_estoque_lotes(id_produto, quantidade)
            
            cursor.execute(
                "UPDATE tbl_estoque SET quantidade_atual = quantidade_atual - %s WHERE id_produto = %s",
                (quantidade, id_produto)
            )

        conexao.commit()
        print(f"✅ Venda #{id_venda} registrada com sucesso! Total: R${valor_total:.2f}")
    except Exception as e:
        conexao.rollback()
        print(f"❌ Erro ao registrar venda: {e}")


def listar_vendas():
    print("\n--- Histórico de Vendas ---")
    try:
        cursor.execute("""
            SELECT id_venda, data_venda, valor_total_venda
            FROM tbl_venda
            ORDER BY data_venda DESC, id_venda DESC
        """)
        vendas = cursor.fetchall()

        if not vendas:
            print("Nenhuma venda registrada.")
            return

        print(f"\n{'ID':<6} {'Data':<12} {'Valor Total':>12}")
        print("-" * 35)
        for v in vendas:
            print(f"{v[0]:<6} {str(v[1]):<12} R${v[2]:>9.2f}")

        ver_detalhes = input("\nVer detalhes de alguma venda? (s/n): ")
        if ver_detalhes.lower() == "s":
            try:
                id_venda = int(input("ID da venda: "))
                detalhar_venda(id_venda)
            except ValueError:
                print("❌ ID inválido. Por favor, digite um número inteiro.")
    except Exception as e:
        print(f"❌ Erro ao listar vendas: {e}")


def detalhar_venda(id_venda):
    try:
        cursor.execute("""
            SELECT p.nome_produto, iv.quantidade_itens, iv.preco_unitario,
                   (iv.quantidade_itens * iv.preco_unitario) AS subtotal
            FROM tbl_item_venda iv
            JOIN tbl_produtos p ON iv.id_produto = p.id_produtos
            WHERE iv.id_venda = %s
        """, (id_venda,))
        itens = cursor.fetchall()

        if not itens:
            print("Venda não encontrada.")
            return

        print(f"\n--- Detalhes da Venda #{id_venda} ---")
        print(f"{'Produto':<25} {'Qtd':>5} {'Preço Unit':>12} {'Subtotal':>12}")
        print("-" * 58)
        for item in itens:
            print(f"{item[0]:<25} {item[1]:>5} R${item[2]:>9.2f} R${item[3]:>9.2f}")
    except Exception as e:
        print(f"❌ Erro ao detalhar venda: {e}")


# ================================================
#               FUNÇÕES - FORNECEDORES
# ================================================

def adicionar_fornecedor():
    print("\n--- Adicionar Fornecedor ---")
    nome = input("Nome do fornecedor: ")
    telefone = input("Telefone: ")
    email = input("E-mail: ")
    endereco = input("Endereço: ")

    try:
        sql = """
            INSERT INTO tbl_fornecedor (nome_fornecedor, telefone_fornecedor, email_fornecedor, endereco_fornecedor)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (nome, telefone, email, endereco))
        conexao.commit()
        print(f"✅ Fornecedor '{nome}' adicionado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao adicionar fornecedor: {e}")


def listar_fornecedores():
    print("\n--- Lista de Fornecedores ---")
    try:
        cursor.execute("SELECT id_fornecedor, nome_fornecedor, telefone_fornecedor, email_fornecedor, endereco_fornecedor FROM tbl_fornecedor ORDER BY id_fornecedor")
        fornecedores = cursor.fetchall()

        if not fornecedores:
            print("Nenhum fornecedor cadastrado.")
            return

        print(f"\n{'ID':<5} {'Nome':<25} {'Telefone':<15} {'E-mail':<25} {'Endereço'}")
        print("-" * 90)
        for f in fornecedores:
            print(f"{f[0]:<5} {str(f[1]):<25} {str(f[2]):<15} {str(f[3]):<25} {f[4]}")
    except Exception as e:
        print(f"❌ Erro ao listar fornecedores: {e}")


def excluir_fornecedor():
    print("\n--- Excluir Fornecedor ---")
    listar_fornecedores()
    try:
        id_forn = int(input("\nDigite o ID do fornecedor a excluir: "))
        confirmacao = input(f"Confirmar exclusão do fornecedor ID {id_forn}? (s/n): ")
        if confirmacao.lower() != "s":
            print("Operação cancelada.")
            return

        cursor.execute("DELETE FROM tbl_fornecedor WHERE id_fornecedor = %s", (id_forn,))
        conexao.commit()

        if cursor.rowcount > 0:
            print("✅ Fornecedor excluído com sucesso!")
        else:
            print("❌ Fornecedor não encontrado.")
    except ValueError:
        print("❌ ID inválido.")
    except Exception as e:
        print(f"❌ Erro ao excluir fornecedor: {e}")


def atualizar_fornecedor():
    print("\n--- Atualizar Fornecedor ---")
    listar_fornecedores()
    try:
        id_forn = int(input("\nDigite o ID do fornecedor que deseja atualizar: "))

        nome = input("Novo nome (deixe em branco para manter): ")
        telefone = input("Novo telefone (deixe em branco para manter): ")
        email = input("Novo e-mail (deixe em branco para manter): ")
        endereco = input("Novo endereço (deixe em branco para manter): ")

        cursor.execute("SELECT nome_fornecedor, telefone_fornecedor, email_fornecedor, endereco_fornecedor FROM tbl_fornecedor WHERE id_fornecedor = %s", (id_forn,))
        atual = cursor.fetchone()
        if not atual:
            print("❌ Fornecedor não encontrado.")
            return

        nome = nome if nome else atual[0]
        telefone = telefone if telefone else atual[1]
        email = email if email else atual[2]
        endereco = endereco if endereco else atual[3]

        sql = """
            UPDATE tbl_fornecedor
            SET nome_fornecedor = %s, telefone_fornecedor = %s, email_fornecedor = %s, endereco_fornecedor = %s
            WHERE id_fornecedor = %s
        """
        cursor.execute(sql, (nome, telefone, email, endereco, id_forn))
        conexao.commit()

        if cursor.rowcount > 0:
            print("✅ Fornecedor atualizado com sucesso!")
        else:
            print("❌ Fornecedor não encontrado.")
    except ValueError:
        print("❌ ID inválido.")
    except Exception as e:
        print(f"❌ Erro ao atualizar fornecedor: {e}")


# ================================================
#               MENU PRINCIPAL
# ================================================

def menu_produtos():
    while True:
        print("\n==== PRODUTOS ====")
        print("1 - Adicionar produto")
        print("2 - Listar produtos")
        print("3 - Atualizar produto")
        print("4 - Excluir produto")
        print("0 - Voltar")

        opcao = input("Escolha: ")
        if opcao == "1":
            adicionar_produto()
        elif opcao == "2":
            listar_produtos()
        elif opcao == "3":
            atualizar_produto()
        elif opcao == "4":
            excluir_produto()
        elif opcao == "0":
            break
        else:
            print("❌ Opção inválida")


def menu_estoque():
    while True:
        print("\n==== ESTOQUE ====")
        print("1 - Ver estoque (lista de produtos)")
        print("2 - Atualizar quantidade em estoque")
        print("3 - Ver produtos com estoque baixo")
        print("4 - Ver lotes de um produto")
        print("0 - Voltar")

        opcao = input("Escolha: ")
        if opcao == "1":
            listar_produtos()
        elif opcao == "2":
            atualizar_estoque()
        elif opcao == "3":
            verificar_estoque_baixo()
        elif opcao == "4":
            listar_lotes_produto()
        elif opcao == "0":
            break
        else:
            print("❌ Opção inválida")


def menu_vendas():
    while True:
        print("\n==== VENDAS ====")
        print("1 - Registrar nova venda")
        print("2 - Listar vendas")
        print("0 - Voltar")

        opcao = input("Escolha: ")
        if opcao == "1":
            registrar_venda()
        elif opcao == "2":
            listar_vendas()
        elif opcao == "0":
            break
        else:
            print("❌ Opção inválida")


def menu_fornecedores():
    while True:
        print("\n==== FORNECEDORES ====")
        print("1 - Adicionar fornecedor")
        print("2 - Listar fornecedores")
        print("3 - Atualizar fornecedor")
        print("4 - Excluir fornecedor")
        print("0 - Voltar")

        opcao = input("Escolha: ")
        if opcao == "1":
            adicionar_fornecedor()
        elif opcao == "2":
            listar_fornecedores()
        elif opcao == "3":
            atualizar_fornecedor()
        elif opcao == "4":
            excluir_fornecedor()
        elif opcao == "0":
            break
        else:
            print("❌ Opção inválida")


# ================================================
#               FUNÇÕES - RELATÓRIOS
# ================================================

def relatorio_faturamento():
    print("\n--- Resumo de Faturamento ---")
    try:
        cursor.execute("SELECT COUNT(id_venda), SUM(valor_total_venda) FROM tbl_venda")
        row = cursor.fetchone()
        total_vendas = row[0] if row and row[0] is not None else 0
        faturamento = row[1] if row and row[1] is not None else 0.0

        print(f"\nTotal de vendas realizadas: {total_vendas}")
        print(f"Faturamento bruto total: R${faturamento:.2f}")
    except Exception as e:
        print(f"❌ Erro ao gerar relatório de faturamento: {e}")


def relatorio_produtos_mais_vendidos():
    print("\n--- Produtos Mais Vendidos ---")
    try:
        sql = """
            SELECT p.id_produtos, p.nome_produto, SUM(iv.quantidade_itens) AS total_vendido,
                   SUM(iv.quantidade_itens * iv.preco_unitario) AS receita_gerada
            FROM tbl_item_venda iv
            JOIN tbl_produtos p ON iv.id_produto = p.id_produtos
            GROUP BY p.id_produtos, p.nome_produto
            ORDER BY total_vendido DESC
            LIMIT 10
        """
        cursor.execute(sql)
        itens = cursor.fetchall()

        if not itens:
            print("Nenhuma venda registrada até o momento.")
            return

        print(f"\n{'ID':<5} {'Nome do Produto':<30} {'Qtd Vendida':>12} {'Receita Gerada':>15}")
        print("-" * 66)
        for item in itens:
            print(f"{item[0]:<5} {item[1]:<30} {item[2]:>12} R${item[3]:>12.2f}")
    except Exception as e:
        print(f"❌ Erro ao gerar relatório de produtos mais vendidos: {e}")


def relatorio_alertas_lotes():
    print("\n--- ⚠️ Alertas de Validade de Lotes ---")
    try:
        sql_vencidos = """
            SELECT p.nome_produto, l.numero_lote, l.quantidade_lote, l.data_validade
            FROM tbl_lotes l
            JOIN tbl_produtos p ON l.id_produto = p.id_produtos
            WHERE l.data_validade < CURDATE() AND l.quantidade_lote > 0
            ORDER BY l.data_validade ASC
        """
        cursor.execute(sql_vencidos)
        vencidos = cursor.fetchall()

        sql_a_vencer = """
            SELECT p.nome_produto, l.numero_lote, l.quantidade_lote, l.data_validade,
                   DATEDIFF(l.data_validade, CURDATE()) AS dias_restantes
            FROM tbl_lotes l
            JOIN tbl_produtos p ON l.id_produto = p.id_produtos
            WHERE l.data_validade >= CURDATE() 
              AND l.data_validade <= DATE_ADD(CURDATE(), INTERVAL 30 DAY) 
              AND l.quantidade_lote > 0
            ORDER BY l.data_validade ASC
        """
        cursor.execute(sql_a_vencer)
        a_vencer = cursor.fetchall()

        print("\n🚨 LOTES VENCIDOS:")
        if not vencidos:
            print("✅ Nenhum lote vencido em estoque!")
        else:
            print(f"{'Produto':<25} {'Lote':<15} {'Qtd':>8} {'Validade':<12}")
            print("-" * 62)
            for v in vencidos:
                print(f"{v[0]:<25} {v[1]:<15} {v[2]:>8} {str(v[3]):<12}")

        print("\n⚠️ LOTES A VENCER NOS PRÓXIMOS 30 DIAS:")
        if not a_vencer:
            print("✅ Nenhum lote próximo do vencimento!")
        else:
            print(f"{'Produto':<25} {'Lote':<15} {'Qtd':>8} {'Validade':<12} {'Dias Restantes'}")
            print("-" * 75)
            for av in a_vencer:
                print(f"{av[0]:<25} {av[1]:<15} {av[2]:>8} {str(av[3]):<12} {av[4]} dias")

    except Exception as e:
        print(f"❌ Erro ao gerar alertas de validade de lotes: {e}")


def menu_relatorios():
    while True:
        print("\n==== RELATÓRIOS ====")
        print("1 - Resumo de faturamento")
        print("2 - Produtos mais vendidos")
        print("3 - Alertas de validade de lotes")
        print("0 - Voltar")

        opcao = input("Escolha: ")
        if opcao == "1":
            relatorio_faturamento()
        elif opcao == "2":
            relatorio_produtos_mais_vendidos()
        elif opcao == "3":
            relatorio_alertas_lotes()
        elif opcao == "0":
            break
        else:
            print("❌ Opção inválida")


def menu():
    while True:
        print("\n" + "=" * 40)
        print("       🏪 SmartStock - Sistema de Estoque")
        print("=" * 40)
        print("1 - 📦 Produtos")
        print("2 - 🗃️  Estoque")
        print("3 - 💰 Vendas")
        print("4 - 🚚 Fornecedores")
        print("5 - 📊 Relatórios")
        print("0 - 🚪 Sair")
        print("=" * 40)

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            menu_produtos()
        elif opcao == "2":
            menu_estoque()
        elif opcao == "3":
            menu_vendas()
        elif opcao == "4":
            menu_fornecedores()
        elif opcao == "5":
            menu_relatorios()
        elif opcao == "0":
            print("\n👋 Encerrando o SmartStock. Até logo!")
            cursor.close()
            conexao.close()
            break
        else:
            print("❌ Opção inválida")


# ---------------- EXECUÇÃO ---------------- #

if __name__ == "__main__":
    menu()