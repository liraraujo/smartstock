import mysql.connector

# ---------------- CONEXÃO ---------------- #

conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="smart_stock"
)

cursor = conexao.cursor()

# ---------------- FUNÇÕES (IMPLEMENTAR) ---------------- #

def adicionar_produto():
    nome = input('Digite o nome do produto: ')
    descricao = input('Digite a descrição do produto: ')
    preco = float(input('Digite o preço: '))
    categoria = input("Digite a categoria: ")

    sql = """ INSERT INTO tbl_produtos (nome_produto, descricao_produto, preco_produto, categoria_produto) VALUES (%s, %s, %s, %s)"""
    valores = (nome, descricao, preco, categoria)
    cursor.execute(sql, valores)
    conexao.commit()
    


def listar_produtos():
    # TODO: buscar e mostrar produtos
    pass


def atualizar_produto():
    # TODO: atualizar produto pelo ID
    pass


def excluir_produto():
    # TODO: deletar produto pelo ID
    pass


# ---------------- MENU ---------------- #

def menu():
    while True:
        print("\n==== MENU ====")
        print("1 - Adicionar produto")
        print("2 - Listar produtos")
        print("3 - Atualizar produto")
        print("4 - Excluir produto")
        print("0 - Sair")

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
            print("Saindo...")
            break

        else:
            print("❌ Opção inválida")


# ---------------- EXECUÇÃO ---------------- #

if __name__ == "__main__":
    menu()