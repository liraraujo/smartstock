CREATE DATABASE smart_stock;
USE smart_stock;

CREATE TABLE tbl_produtos (
   id_produtos INT AUTO_INCREMENT PRIMARY KEY,
   nome_produto VARCHAR (100),
   descricao_produto TEXT,
   preco_produto DECIMAL (10,2),
   categoria_produto VARCHAR (100)
);

CREATE TABLE tbl_estoque (
   id_estoque INT AUTO_INCREMENT PRIMARY KEY,
   id_produto INT,
   quantidade_atual INT,
   quantidade_minima INT,
   FOREIGN KEY (id_produto) REFERENCES tbl_produtos(id_produtos)
);

CREATE TABLE tbl_venda (
   id_venda INT AUTO_INCREMENT PRIMARY KEY,
   data_venda DATE,
   valor_total_venda DECIMAL (10,2)
);

CREATE TABLE tbl_item_venda (
   id_item INT AUTO_INCREMENT PRIMARY KEY,
   id_venda INT,
   id_produto INT,
   quantidade_itens INT,
   preco_unitario DECIMAL (10,2),
   FOREIGN KEY (id_venda) REFERENCES tbl_venda(id_venda),
   FOREIGN KEY (id_produto) REFERENCES tbl_produtos(id_produtos)
);

CREATE TABLE tbl_fornecedor (
   id_fornecedor INT AUTO_INCREMENT PRIMARY KEY,
   nome_fornecedor TEXT,
   telefone_fornecedor VARCHAR (50),
   email_fornecedor VARCHAR (100),
   endereco_fornecedor VARCHAR (100)
);