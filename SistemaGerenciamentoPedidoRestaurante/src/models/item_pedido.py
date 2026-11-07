"""Modelo de dados para a entidade ItemPedido."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ItemPedido:
    """Representa a associação de um prato a um pedido com quantidade e valor."""

    id: int
    pedido_id: int
    item_cardapio_id: int
    quantidade: int
    preco_unitario: float
    observacao: Optional[str] = None
    nome_item: Optional[str] = None
    codigo_item: Optional[str] = None

    def subtotal(self) -> float:
        """Calcula o valor subtotal do item multiplicado pela quantidade."""
        return self.quantidade * self.preco_unitario
