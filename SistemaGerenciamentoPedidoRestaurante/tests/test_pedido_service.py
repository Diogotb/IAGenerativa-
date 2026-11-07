"""Testes unitários para o serviço de pedidos e fechamento."""

from src.config.database import inicializar_banco_dados
from src.services.pedido_service import (
    criar_pedido_com_item,
    adicionar_item_a_pedido,
    obter_pedido_por_id,
    atualizar_status_pedido,
    liquidar_conta_mesa,
)
from src.services.mesa_service import obter_mesa_por_numero


def setup_module() -> None:
    """Prepara o banco de dados antes da execução dos testes."""
    inicializar_banco_dados()


def test_fluxo_completo_pedido() -> None:
    """Testa abertura, acréscimo de item, troca de status e fechamento."""
    sucesso, msg, pid = criar_pedido_com_item(5, "RIS-01", 2, "Sem sal")
    assert sucesso is True
    assert pid is not None
    mesa = obter_mesa_por_numero(5)
    assert mesa.status == "OCUPADA"

    suc_add, _ = adicionar_item_a_pedido(pid, "SUC-02", 1)
    assert suc_add is True

    suc_st, _ = atualizar_status_pedido(pid, "PREPARANDO")
    assert suc_st is True

    ped = obter_pedido_por_id(pid)
    assert ped.status == "PREPARANDO"
    assert len(ped.itens) == 2

    suc_liq, _, valor = liquidar_conta_mesa(pid, 5, aplicar_taxa=True)
    assert suc_liq is True
    assert valor > 0
    mesa_liberada = obter_mesa_por_numero(5)
    assert mesa_liberada.status == "LIVRE"


def test_criar_pedido_quantidade_invalida() -> None:
    """Impede criação de pedidos com quantidade zero ou negativa."""
    sucesso, msg, pid = criar_pedido_com_item(1, "RIS-01", 0)
    assert sucesso is False
    assert pid is None
