"""Modelo de dados para a entidade ItemCardapio."""

from dataclasses import dataclass


@dataclass
class ItemCardapio:
    """Representa um prato ou bebida disponível no restaurante."""

    id: int
    codigo: str
    nome: str
    categoria: str
    preco: float
    disponivel: bool

    def preco_formatado(self) -> str:
        """Formata o valor monetário no padrão brasileiro."""
        return f"R$ {self.preco:.2f}".replace(".", ",")
