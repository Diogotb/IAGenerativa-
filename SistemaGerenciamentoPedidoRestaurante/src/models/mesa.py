"""Modelo de dados para a entidade Mesa."""

from dataclasses import dataclass


@dataclass
class Mesa:
    """Representa uma mesa de atendimento no restaurante."""

    id: int
    numero: int
    capacidade: int
    status: str

    def esta_livre(self) -> bool:
        """Verifica se a mesa está disponível para novos clientes."""
        return self.status == "LIVRE"

    def esta_ocupada(self) -> bool:
        """Verifica se a mesa está em atendimento ativo."""
        return self.status == "OCUPADA"
