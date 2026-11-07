"""Modelo de dados para a entidade Pedido."""

from dataclasses import dataclass, field
from typing import List, Optional
from src.models.item_pedido import ItemPedido


@dataclass
class Pedido:
    """Representa a comanda de uma mesa com itens e status de produção."""

    id: int
    mesa_id: int
    data_hora: str
    status: str
    valor_total: float
    mesa_numero: Optional[int] = None
    itens: List[ItemPedido] = field(default_factory=list)

    def em_aberto(self) -> bool:
        """Verifica se o pedido ainda não foi liquidado ou cancelado."""
        return self.status not in ("PAGO", "CANCELADO")

    def total_itens(self) -> int:
        """Calcula a soma das quantidades de todos os itens da comanda."""
        return sum(item.quantidade for item in self.itens)
