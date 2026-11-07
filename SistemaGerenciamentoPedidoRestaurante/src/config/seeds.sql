-- Inserção de dados iniciais para mesas
INSERT OR IGNORE INTO mesas (id, numero, capacidade, status) VALUES
(1, 1, 2, 'LIVRE'),
(2, 2, 4, 'OCUPADA'),
(3, 3, 4, 'RESERVADA'),
(4, 4, 4, 'LIVRE'),
(5, 5, 6, 'LIVRE');

-- Inserção de itens do cardápio
INSERT OR IGNORE INTO cardapio (id, codigo, nome, categoria, preco, disponivel) VALUES
(1, 'ENT-01', 'Bruschetta Tradicional', 'Entradas', 28.00, 1),
(2, 'RIS-01', 'Risoto de Funghi', 'Pratos Principais', 58.50, 1),
(3, 'MAS-01', 'Fettuccine ao Pesto', 'Pratos Principais', 52.00, 1),
(4, 'SUC-01', 'Suco de Laranja Natural', 'Bebidas', 10.00, 1),
(5, 'SUC-02', 'Suco de Maracujá', 'Bebidas', 12.00, 1),
(6, 'SOB-01', 'Tiramisù Clássico', 'Sobremesas', 26.00, 1);
