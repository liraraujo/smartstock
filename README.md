# 🏪 SmartStock — Sistema de Gestão de Estoque

> Sistema de controle de estoque via terminal, desenvolvido em Python com integração ao banco de dados MySQL. Gerencia produtos, lotes, vendas, fornecedores e gera relatórios completos.

---

## 📋 Índice

- [Funcionalidades](#-funcionalidades)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação e Configuração](#-instalação-e-configuração)
- [Como Executar](#-como-executar)
- [Guia de Uso](#-guia-de-uso)
  - [Menu Principal](#menu-principal)
  - [Produtos](#-produtos)
  - [Estoque](#️-estoque)
  - [Vendas](#-vendas)
  - [Fornecedores](#-fornecedores)
  - [Relatórios](#-relatórios)
- [Estrutura do Banco de Dados](#-estrutura-do-banco-de-dados)
- [Estrutura de Arquivos](#-estrutura-de-arquivos)

---

## ✨ Funcionalidades

| Módulo        | Funcionalidades                                                                 |
|---------------|---------------------------------------------------------------------------------|
| 📦 Produtos   | Cadastrar, listar, atualizar e excluir produtos                                 |
| 🗃️ Estoque   | Entradas e saídas de estoque, alerta de estoque baixo, controle por lotes       |
| 💰 Vendas     | Registrar vendas com múltiplos itens, histórico e detalhamento                  |
| 🚚 Fornecedores | Cadastrar, listar, atualizar e excluir fornecedores                           |
| 📊 Relatórios | Faturamento geral, produtos mais vendidos, alertas de validade de lotes (FEFO)  |

**Destaques técnicos:**
- 🔄 **Controle FEFO** *(First Expired, First Out)*: saídas de estoque são deduzidas automaticamente do lote com vencimento mais próximo.
- ⚠️ **Alertas de Estoque Baixo**: identifica produtos abaixo da quantidade mínima configurada.
- 🚨 **Alertas de Validade**: exibe lotes vencidos e lotes a vencer nos próximos 30 dias.

---

## 🛠️ Pré-requisitos

- **Python 3.8+**
- **MySQL Server 8.0+** (ou MariaDB compatível)
- Biblioteca Python `mysql-connector-python`

### Instalando a dependência Python

```bash
pip install mysql-connector-python
```

---

## ⚙️ Instalação e Configuração

### 1. Clone ou baixe o projeto

```bash
git clone https://github.com/seu-usuario/smartstock-2.git
cd smartstock-2
```

### 2. Crie o banco de dados

Abra o MySQL e execute o script de criação:

```bash
mysql -u root -p < bdsmart.sql
```

Ou, pelo MySQL Workbench / terminal MySQL, rode o conteúdo de `bdsmart.sql`:

```sql
CREATE DATABASE smart_stock;
USE smart_stock;
-- (restante do script cria as tabelas automaticamente)
```

### 3. (Opcional) Popule com dados de exemplo

Para iniciar com 24 produtos, 8 fornecedores e 5 vendas de exemplo já cadastrados:

```bash
mysql -u root -p smart_stock < popular_bdsmart.sql
```

> ⚠️ **Atenção:** este script limpa as tabelas antes de inserir. Use apenas em ambiente de testes.

### 4. Configure a conexão no código

Abra o arquivo `smart.py` e ajuste as credenciais do banco de dados na seção de conexão (linhas 12–18):

```python
conexao = mysql.connector.connect(
    host="localhost",      # endereço do servidor MySQL
    user="root",           # usuário do MySQL
    password="root",       # senha do MySQL
    database="smart_stock" # nome do banco de dados
)
```

---

## ▶️ Como Executar

```bash
python smart.py
```

Se a conexão for bem-sucedida, você verá:

```
✅ Conectado ao banco de dados com sucesso!

========================================
       🏪 SmartStock - Sistema de Estoque
========================================
1 - 📦 Produtos
2 - 🗃️  Estoque
3 - 💰 Vendas
4 - 🚚 Fornecedores
5 - 📊 Relatórios
0 - 🚪 Sair
========================================
Escolha uma opção:
```

---

## 📖 Guia de Uso

### Menu Principal

Navegue digitando o **número da opção** e pressionando **Enter**. Para voltar ao menu anterior, sempre pressione `0`.

---

### 📦 Produtos

**Opção `1` no menu principal**

| Opção | Ação               | O que é pedido                                                                                      |
|-------|--------------------|-----------------------------------------------------------------------------------------------------|
| `1`   | Adicionar produto  | Nome, descrição, preço, categoria, quantidade inicial, quantidade mínima, lote e data de validade   |
| `2`   | Listar produtos    | Exibe tabela com ID, nome, categoria, preço, estoque atual, mínimo, próximo vencimento e status     |
| `3`   | Atualizar produto  | ID do produto + novos valores (deixe em branco para manter o valor atual)                           |
| `4`   | Excluir produto    | ID do produto + confirmação (`s` para confirmar)                                                    |

**Exemplo — Adicionar um produto:**
```
--- Adicionar Produto ---
Digite o nome do produto: Leite Integral 1L
Digite a descrição do produto: Caixa de leite UHT 1 litro
Digite o preço: R$ 4.80
Digite a categoria: Laticínios
Digite a quantidade inicial em estoque: 100
Digite a quantidade mínima em estoque (alerta): 30
Data de validade do lote inicial (AAAA-MM-DD) ou deixe em branco se não houver: 2026-09-01
Nome/Número do lote inicial (ou Enter para 'LOTE-INICIAL'): LEITE-L01

✅ Produto 'Leite Integral 1L' adicionado com sucesso! (ID: 25)
```

---

### 🗃️ Estoque

**Opção `2` no menu principal**

| Opção | Ação                       | Descrição                                                              |
|-------|----------------------------|------------------------------------------------------------------------|
| `1`   | Ver estoque                | Lista todos os produtos com quantidade atual, mínima e status          |
| `2`   | Atualizar quantidade       | Entrada (`1`) ou saída (`2`) de estoque — saídas usam regra **FEFO**   |
| `3`   | Ver produtos com estoque baixo | Exibe apenas produtos com quantidade atual ≤ quantidade mínima     |
| `4`   | Ver lotes de um produto    | Mostra todos os lotes ativos (com quantidade > 0) de um produto        |

**Exemplo — Dar entrada de estoque:**
```
--- Atualizar Estoque ---
Digite o ID do produto: 1
1 - Adicionar ao estoque (entrada)
2 - Remover do estoque (saída)
Escolha o tipo: 1
Quantidade: 50
Número/Código do lote: LEITE-L03
Data de validade do lote (AAAA-MM-DD) ou deixe em branco se não houver: 2026-10-01

✅ Entrada registrada com sucesso no lote 'LEITE-L03'!
```

**Exemplo — Dar saída de estoque (FEFO automático):**
```
Escolha o tipo: 2
Quantidade: 30
   Dedução no lote 'LEITE-L01': -30 unidades.

✅ Saída de estoque concluída com sucesso!
```

---

### 💰 Vendas

**Opção `3` no menu principal**

| Opção | Ação             | Descrição                                                           |
|-------|------------------|---------------------------------------------------------------------|
| `1`   | Registrar venda  | Adiciona múltiplos produtos à venda; confirma e registra no banco   |
| `2`   | Listar vendas    | Exibe histórico de vendas com opção de ver detalhes por ID          |

**Exemplo — Registrar uma venda:**
```
--- Registrar Nova Venda ---
[lista de produtos é exibida automaticamente]

Digite o ID do produto (ou 0 para finalizar): 7
Produto: Dipirona 500mg cx 20cp | Preço: R$12.00 | Disponível: 250
Quantidade: 10
✅ Item adicionado. Subtotal: R$120.00

Digite o ID do produto (ou 0 para finalizar): 0

💰 Valor total da venda: R$120.00
Confirmar venda? (s/n): s

✅ Venda #6 registrada com sucesso! Total: R$120.00
```

---

### 🚚 Fornecedores

**Opção `4` no menu principal**

| Opção | Ação                  | O que é pedido                              |
|-------|-----------------------|---------------------------------------------|
| `1`   | Adicionar fornecedor  | Nome, telefone, e-mail e endereço           |
| `2`   | Listar fornecedores   | Tabela com todos os fornecedores cadastrados|
| `3`   | Atualizar fornecedor  | ID + novos dados (deixe em branco p/ manter)|
| `4`   | Excluir fornecedor    | ID + confirmação                            |

---

### 📊 Relatórios

**Opção `5` no menu principal**

| Opção | Relatório                   | Descrição                                                              |
|-------|-----------------------------|------------------------------------------------------------------------|
| `1`   | Resumo de faturamento       | Total de vendas realizadas e faturamento bruto acumulado               |
| `2`   | Produtos mais vendidos      | Top 10 produtos por quantidade vendida e receita gerada                |
| `3`   | Alertas de validade de lotes| Lista lotes **vencidos** e lotes que vencem nos **próximos 30 dias**   |

**Exemplo — Alerta de validade:**
```
--- ⚠️ Alertas de Validade de Lotes ---

🚨 LOTES VENCIDOS:
Produto                   Lote            Qtd      Validade
--------------------------------------------------------------
Paracetamol 750mg cx 24cp PARAC-V01        80   2026-05-15
Álcool 70% Antisséptico 1L ALC70-V01       50   2026-05-10

⚠️ LOTES A VENCER NOS PRÓXIMOS 30 DIAS:
Produto                   Lote            Qtd      Validade     Dias Restantes
---------------------------------------------------------------------------
Iogurte Natural 170g      IOGURT-A01       60   2026-05-28    3 dias
```

---

## 🗄️ Estrutura do Banco de Dados

```
smart_stock
│
├── tbl_produtos       — Cadastro de produtos (nome, descrição, preço, categoria)
├── tbl_estoque        — Quantidade atual e mínima por produto (1 registro por produto)
├── tbl_lotes          — Lotes de entrada: número, quantidade, validade, data de entrada
├── tbl_venda          — Cabeçalho das vendas (data e valor total)
├── tbl_item_venda     — Itens de cada venda (produto, quantidade, preço unitário)
└── tbl_fornecedor     — Cadastro de fornecedores (nome, telefone, e-mail, endereço)
```

**Diagrama de relacionamentos:**

```
tbl_fornecedor   tbl_produtos ──── tbl_estoque
                     │    └──────── tbl_lotes
                     │
                 tbl_item_venda
                     │
                 tbl_venda
```

---

## 📁 Estrutura de Arquivos

```
smartstock-2/
│
├── smart.py              # Código principal da aplicação
├── bdsmart.sql           # Script de criação do banco de dados e tabelas
├── popular_bdsmart.sql   # Script de dados de exemplo (24 produtos, 8 fornecedores, 5 vendas)
└── README.md             # Esta documentação
```

---

## 🔧 Solução de Problemas

| Erro                                      | Causa provável                            | Solução                                                      |
|-------------------------------------------|-------------------------------------------|--------------------------------------------------------------|
| `❌ Erro ao conectar ao banco de dados`   | Credenciais incorretas ou MySQL parado    | Verifique usuário/senha e se o serviço MySQL está rodando    |
| `ModuleNotFoundError: mysql.connector`    | Biblioteca não instalada                  | Execute `pip install mysql-connector-python`                 |
| `❌ Estoque insuficiente!`               | Quantidade solicitada maior que o estoque | Verifique a quantidade disponível antes da saída/venda       |
| Caracteres especiais exibidos errado      | Encoding do terminal                      | Use terminal com suporte a UTF-8 (ex: Windows Terminal)      |

---

*Desenvolvido com Python 3 + MySQL*
