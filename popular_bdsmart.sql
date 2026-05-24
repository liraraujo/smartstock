USE smart_stock;

-- ================================================
-- LIMPEZA DAS TABELAS ANTES DE INSERIR
-- ================================================
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE tbl_item_venda;
TRUNCATE tbl_venda;
TRUNCATE tbl_lotes;
TRUNCATE tbl_estoque;
TRUNCATE tbl_produtos;
TRUNCATE tbl_fornecedor;
SET FOREIGN_KEY_CHECKS = 1;


-- ================================================
-- 1. FORNECEDORES (8 fornecedores)
-- ================================================
INSERT INTO tbl_fornecedor (id_fornecedor, nome_fornecedor, telefone_fornecedor, email_fornecedor, endereco_fornecedor) VALUES
(1, 'Distribuidora Laticínios Silva',    '(11) 98888-7777', 'contato@latsilva.com.br',      'Av. das Nações, 1500 - São Paulo/SP'),
(2, 'Tech & Cia Importadora',            '(21) 3444-5555',  'vendas@techcia.com',            'Rua Chile, 50 - Rio de Janeiro/RJ'),
(3, 'Metalúrgica Parafuso Certo',        '(31) 2555-1234',  'comercial@parafusocerto.com',   'Av. Industrial, 800 - Belo Horizonte/MG'),
(4, 'Distribuidora Farma Central',       '(11) 3210-9090',  'pedidos@farmacentral.com.br',   'Rua da Saúde, 300 - Santo André/SP'),
(5, 'Limpeza & Cia Distribuidora',       '(41) 3201-5678',  'vendas@limpezacia.com.br',      'Av. Higienópolis, 450 - Curitiba/PR'),
(6, 'Padaria e Distribuidora Pão Quente','(11) 91234-5678', 'comercial@paoquente.com.br',    'Rua das Flores, 12 - São Paulo/SP'),
(7, 'EPI Segurança Total',               '(48) 3302-9900',  'epi@segurancatotal.com',        'Rod. SC-401, 2100 - Florianópolis/SC'),
(8, 'Escritório Total Distribuidora',    '(62) 3100-4444',  'falecom@escritoriototal.com',   'Rua 1, Setor Industrial - Goiânia/GO');


-- ================================================
-- 2. PRODUTOS (24 produtos de categorias diversas)
-- ================================================
INSERT INTO tbl_produtos (id_produtos, nome_produto, descricao_produto, preco_produto, categoria_produto) VALUES
-- Laticínios (perecíveis)
(1,  'Leite Integral UHT 1L',        'Caixa de leite integral de 1 litro',                    4.80,  'Laticínios'),
(2,  'Iogurte Natural 170g',         'Iogurte natural integral copinho 170g',                  3.50,  'Laticínios'),
(3,  'Queijo Mussarela 500g',        'Queijo mussarela fatiado embalagem a vácuo',             18.90, 'Laticínios'),
(4,  'Manteiga sem Sal 200g',        'Manteiga com e sem sal tablete 200g',                    8.90,  'Laticínios'),
(5,  'Creme de Leite 200ml',         'Creme de leite caixinha 200ml 25% gordura',              5.20,  'Laticínios'),

-- Padaria (perecíveis, validade muito curta)
(6,  'Pão Francês (kg)',             'Pão francês artesanal vendido por quilograma',           14.00, 'Padaria'),

-- Farmácia (perecíveis com prazo de validade médio)
(7,  'Dipirona 500mg cx 20cp',       'Analgésico e antitérmico caixa com 20 comprimidos',     12.00, 'Farmácia'),
(8,  'Paracetamol 750mg cx 24cp',    'Analgésico e antitérmico caixa com 24 comprimidos',     11.50, 'Farmácia'),
(9,  'Vitamina C 500mg cx 30cp',     'Suplemento vitamínico caixa com 30 comprimidos',        19.90, 'Farmácia'),

-- Eletrônicos (não perecíveis)
(10, 'Teclado Mecânico USB',         'Teclado mecânico RGB switch azul ABNT2',                189.90,'Eletrônicos'),
(11, 'Mouse Sem Fio 2.4GHz',         'Mouse sem fio com pilha AA 1200 DPI preto',             89.90, 'Eletrônicos'),
(12, 'Monitor LED 24" Full HD',      'Monitor LED 24 polegadas resolução 1920x1080 60Hz',     799.00,'Eletrônicos'),
(13, 'Cabo HDMI 2m',                 'Cabo HDMI 2.0 4K macho-macho 2 metros',                 25.00, 'Eletrônicos'),
(14, 'Carregador USB-C 65W',         'Carregador compacto USB-C 65W com cabo 1m',             45.00, 'Eletrônicos'),
(15, 'Pen Drive 64GB USB 3.0',       'Pen drive 64GB velocidade de leitura até 130 MB/s',     35.00, 'Eletrônicos'),

-- Ferramentas (não perecíveis)
(16, 'Martelo de Unha 29mm',         'Martelo aço carbono com cabo de fibra de vidro',        45.00, 'Ferramentas'),
(17, 'Chave de Fenda Phillips 5mm',  'Chave de fenda ponta Phillips 1/4" cabo emborrachado',  22.50, 'Ferramentas'),
(18, 'Parafuso Philips 4.5x40 cx100','Caixa com 100 parafusos philips zincados 4.5x40mm',     18.00, 'Ferramentas'),
(19, 'Fita Isolante Scotch 15m',     'Fita isolante autofusão 15 metros preta',               9.00,  'Ferramentas'),

-- EPI (não perecíveis)
(20, 'Luva de Segurança Nitrílica',  'Luva nitrílica antiderrapante CA 44703 tamanho M',      15.00, 'EPI'),

-- Material de Escritório (não perecíveis)
(21, 'Resma Papel Sulfite A4 500fls','Resma 500 folhas papel sulfite A4 75g/m²',              28.00, 'Escritório'),
(22, 'Caneta Esferográfica Azul cx12','Caixa com 12 canetas esferográficas 0.5mm azul',        8.50,  'Escritório'),

-- Limpeza (perecíveis com validade)
(23, 'Detergente Neutro 500ml',      'Detergente neutro concentrado glicerinado 500ml',       5.50,  'Limpeza'),
(24, 'Álcool 70% Antisséptico 1L',   'Álcool etílico 70% em solução aquosa 1 litro',          14.00, 'Limpeza');


-- ================================================
-- 3. ESTOQUE CONSOLIDADO (um registro por produto)
-- A quantidade_atual DEVE SER a SOMA de todos os lotes ativos de cada produto.
-- ================================================
INSERT INTO tbl_estoque (id_produto, quantidade_atual, quantidade_minima) VALUES
--  id    atual  min     Situação
(1,  300,  100),  -- Leite: OK
(2,  100,   30),  -- Iogurte: OK
(3,   60,   20),  -- Queijo: OK
(4,   80,   20),  -- Manteiga: OK
(5,  120,   40),  -- Creme de Leite: OK
(6,   30,   10),  -- Pão Francês: OK (validade curtíssima!)
(7,  250,   50),  -- Dipirona: OK
(8,  200,   50),  -- Paracetamol: OK
(9,   90,   30),  -- Vitamina C: OK
(10,  12,    5),  -- Teclado: OK
(11,  20,    5),  -- Mouse: OK
(12,   6,    2),  -- Monitor: OK
(13,  35,   10),  -- Cabo HDMI: OK
(14,  18,    5),  -- Carregador: OK
(15,  45,   10),  -- Pen Drive: OK
(16,   8,   10),  -- Martelo: ⚠️ ESTOQUE BAIXO (8 < 10)
(17,  35,   10),  -- Chave de Fenda: OK
(18, 500,  100),  -- Parafuso: OK
(19,  60,   20),  -- Fita Isolante: OK
(20,  50,   15),  -- Luva: OK
(21,  25,    5),  -- Resma de Papel: OK
(22,  40,   10),  -- Caneta: OK
(23, 140,   30),  -- Detergente: OK
(24, 150,   40);  -- Álcool 70%: OK


-- ================================================
-- 4. LOTES (representação detalhada por entrada)
-- Inclui lotes VENCIDOS, A VENCER e SEM VALIDADE
-- ================================================
INSERT INTO tbl_lotes (id_produto, numero_lote, quantidade_lote, data_validade, data_entrada) VALUES

-- Leite Integral (2 lotes, com validade)
(1, 'LEITE-L01', 200, '2026-07-20', '2026-05-10'),
(1, 'LEITE-L02', 100, '2026-08-15', '2026-05-20'),

-- Iogurte Natural (2 lotes: 1 a vencer em breve, 1 normal)
(2, 'IOGURT-A01',  60, '2026-05-28', '2026-05-08'),  -- ⚠️ Vence em dias!
(2, 'IOGURT-A02',  40, '2026-06-20', '2026-05-18'),

-- Queijo Mussarela (2 lotes, com validade)
(3, 'QUEIJO-M01',  25, '2026-06-05', '2026-05-12'),
(3, 'QUEIJO-M02',  35, '2026-06-30', '2026-05-22'),

-- Manteiga (1 lote, com validade)
(4, 'MANT-S01',    80, '2026-09-01', '2026-04-15'),

-- Creme de Leite (2 lotes, com validade)
(5, 'CREME-L01',   50, '2026-07-10', '2026-04-20'),
(5, 'CREME-L02',   70, '2026-08-30', '2026-05-15'),

-- Pão Francês (1 lote, validade HOJE ou curtíssima)
(6, 'PAO-D01',     30, '2026-05-25', '2026-05-24'),  -- ⚠️ Validade amanhã!

-- Dipirona (2 lotes, com validade longa)
(7, 'DIPIR-01',   100, '2027-03-01', '2026-03-10'),
(7, 'DIPIR-02',   150, '2027-08-15', '2026-05-01'),

-- Paracetamol (1 lote vencido, 1 normal - para acionar alerta!)
(8, 'PARAC-V01',   80, '2026-05-15', '2026-02-01'),  -- 🚨 VENCIDO!
(8, 'PARAC-N02',  120, '2027-05-01', '2026-05-10'),

-- Vitamina C (1 lote, com validade)
(9, 'VITC-001',    90, '2027-01-20', '2026-04-05'),

-- Teclado Mecânico (sem validade)
(10, 'TECL-TM01',  12, NULL, '2026-03-15'),

-- Mouse (sem validade)
(11, 'MOUSE-SF01', 20, NULL, '2026-04-01'),

-- Monitor (sem validade)
(12, 'MONIT-24HD', 6,  NULL, '2026-02-20'),

-- Cabo HDMI (sem validade)
(13, 'CABO-H2M',   35, NULL, '2026-01-10'),

-- Carregador USB-C (sem validade)
(14, 'CARREG-65',  18, NULL, '2026-04-18'),

-- Pen Drive (sem validade)
(15, 'PEND-64G',   45, NULL, '2026-03-22'),

-- Martelo de Unha (sem validade - estoque baixo!)
(16, 'MART-U29',   8,  NULL, '2026-04-10'),

-- Chave de Fenda (2 lotes, sem validade)
(17, 'CHAVE-PH01', 15, NULL, '2026-03-05'),
(17, 'CHAVE-PH02', 20, NULL, '2026-05-01'),

-- Parafuso (sem validade)
(18, 'PARA-P45',  500, NULL, '2026-02-01'),

-- Fita Isolante (sem validade)
(19, 'FITA-SC15',  60, NULL, '2026-04-20'),

-- Luva de Segurança (2 lotes, sem validade)
(20, 'LUVA-NM01',  30, NULL, '2026-03-10'),
(20, 'LUVA-NM02',  20, NULL, '2026-05-05'),

-- Resma de Papel (sem validade)
(21, 'PAPEL-A4',   25, NULL, '2026-03-01'),

-- Caneta (sem validade)
(22, 'CANETA-AZ',  40, NULL, '2026-04-12'),

-- Detergente (2 lotes, com validade)
(23, 'DET-N01',    80, '2026-11-20', '2026-03-15'),
(23, 'DET-N02',    60, '2027-02-10', '2026-05-10'),

-- Álcool 70% (2 lotes, com validade - 1 vencido para teste de alerta!)
(24, 'ALC70-V01',  50, '2026-05-10', '2025-11-01'),  -- 🚨 VENCIDO!
(24, 'ALC70-N02', 100, '2026-12-31', '2026-04-01');


-- ================================================
-- 5. VENDAS E ITENS DE VENDA (5 vendas com 25 itens no total)
-- ================================================

-- Venda #1 - 20/05 - Mix de laticínios, eletrônicos e escritório
INSERT INTO tbl_venda (id_venda, data_venda, valor_total_venda) VALUES
(1, '2026-05-20', 681.80);
INSERT INTO tbl_item_venda (id_venda, id_produto, quantidade_itens, preco_unitario) VALUES
(1, 1,  20, 4.80),   -- 20 Leites
(1, 2,  10, 3.50),   -- 10 Iogurtes
(1, 3,   5, 18.90),  -- 5 Queijos
(1, 10,  1, 189.90), -- 1 Teclado
(1, 22, 10, 8.50);   -- 10 Canetas

-- Venda #2 - 21/05 - Farmácia, eletrônicos e EPI
INSERT INTO tbl_venda (id_venda, data_venda, valor_total_venda) VALUES
(2, '2026-05-21', 1364.50);
INSERT INTO tbl_item_venda (id_venda, id_produto, quantidade_itens, preco_unitario) VALUES
(2, 7,  30, 12.00),  -- 30 Dipirona
(2, 8,  20, 11.50),  -- 20 Paracetamol
(2, 11,  5, 89.90),  -- 5 Mouses
(2, 13, 10, 25.00),  -- 10 Cabos HDMI
(2, 20,  5, 15.00);  -- 5 Luvas

-- Venda #3 - 22/05 - Ferramentas, limpeza e escritório
INSERT INTO tbl_venda (id_venda, data_venda, valor_total_venda) VALUES
(3, '2026-05-22', 2637.50);
INSERT INTO tbl_item_venda (id_venda, id_produto, quantidade_itens, preco_unitario) VALUES
(3, 18, 100, 18.00), -- 100 Caixas de Parafusos
(3, 17,   5, 22.50), -- 5 Chaves de Fenda
(3, 23,  30, 5.50),  -- 30 Detergentes
(3, 24,  20, 14.00), -- 20 Álcoois 70%
(3, 21,  10, 28.00); -- 10 Resmas de Papel

-- Venda #4 - 23/05 - Laticínios variados e eletrônicos premium
INSERT INTO tbl_venda (id_venda, data_venda, valor_total_venda) VALUES
(4, '2026-05-23', 2055.50);
INSERT INTO tbl_item_venda (id_venda, id_produto, quantidade_itens, preco_unitario) VALUES
(4, 4,  15, 8.90),   -- 15 Manteigas
(4, 5,  20, 5.20),   -- 20 Cremes de Leite
(4, 15,  5, 35.00),  -- 5 Pen Drives
(4, 12,  2, 799.00), -- 2 Monitores
(4, 19,  5, 9.00);   -- 5 Fitas Isolantes

-- Venda #5 - 24/05 - Farmácia, eletrônicos e ferramentas
INSERT INTO tbl_venda (id_venda, data_venda, valor_total_venda) VALUES
(5, '2026-05-24', 692.50);
INSERT INTO tbl_item_venda (id_venda, id_produto, quantidade_itens, preco_unitario) VALUES
(5, 9,  10, 19.90),  -- 10 Vitaminas C
(5, 14,  5, 45.00),  -- 5 Carregadores
(5, 16,  3, 45.00),  -- 3 Martelos (agora estoque baixo!)
(5, 1,  20, 4.80),   -- 20 Leites
(5, 2,   5, 3.50);   -- 5 Iogurtes
