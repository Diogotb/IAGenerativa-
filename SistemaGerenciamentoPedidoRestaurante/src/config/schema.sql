-- Ativa a verificação de chaves estrangeiras no SQLite
PRAGMA foreign_keys = ON;

-- Tabela de itens disponíveis no cardápio
CREATE TABLE IF NOT EXISTS cardapio (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT NOT NULL UNIQUE,
    nome TEXT NOT NULL,
    categoria TEXT NOT NULL,
    preco REAL NOT NULL CHECK (preco >= 0),
    disponivel INTEGER NOT NULL DEFAULT 1 CHECK (disponivel IN (0, 1))
);

-- Tabela de controle de mesas do restaurante
CREATE TABLE IF NOT EXISTS mesas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero INTEGER NOT NULL UNIQUE,
    capacidade INTEGER NOT NULL CHECK (capacidade > 0),
    status TEXT NOT NULL DEFAULT 'LIVRE' CHECK (status IN ('LIVRE', 'OCUPADA', 'RESERVADA'))
);

-- Tabela de pedidos associados às mesas
CREATE TABLE IF NOT EXISTS pedidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mesa_id INTEGER NOT NULL,
    data_hora DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status TEXT NOT NULL DEFAULT 'RECEBIDO' CHECK (status IN ('RECEBIDO', 'PREPARANDO', 'PRONTO', 'ENTREGUE', 'PAGO')),
    valor_total REAL NOT NULL DEFAULT 0.0 CHECK (valor_total >= 0),
    FOREIGN KEY (mesa_id) REFERENCES mesas (id) ON DELETE RESTRICT ON UPDATE CASCADE
);

-- Tabela de itens pertencentes a cada pedido
CREATE TABLE IF NOT EXISTS itens_pedido (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pedido_id INTEGER NOT NULL,
    item_cardapio_id INTEGER NOT NULL,
    quantidade INTEGER NOT NULL CHECK (quantidade > 0),
    preco_unitario REAL NOT NULL CHECK (preco_unitario >= 0),
    observacao TEXT,
    FOREIGN KEY (pedido_id) REFERENCES pedidos (id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (item_cardapio_id) REFERENCES cardapio (id) ON DELETE RESTRICT ON UPDATE CASCADE
);

-- Índices para otimização de busca e filtros frequentes
CREATE INDEX IF NOT EXISTS idx_cardapio_categoria ON cardapio (categoria);
CREATE INDEX IF NOT EXISTS idx_cardapio_disponivel ON cardapio (disponivel);
CREATE INDEX IF NOT EXISTS idx_mesas_status ON mesas (status);
CREATE INDEX IF NOT EXISTS idx_pedidos_mesa_id ON pedidos (mesa_id);
CREATE INDEX IF NOT EXISTS idx_pedidos_status ON pedidos (status);
CREATE INDEX IF NOT EXISTS idx_pedidos_data_hora ON pedidos (data_hora);
CREATE INDEX IF NOT EXISTS idx_itens_pedido_pedido_id ON itens_pedido (pedido_id);
CREATE INDEX IF NOT EXISTS idx_itens_pedido_item_cardapio_id ON itens_pedido (item_cardapio_id);
