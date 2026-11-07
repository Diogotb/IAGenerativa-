"""Testes unitários para o serviço de cardápio."""

from src.config.database import inicializar_banco_dados
from src.services.cardapio_service import listar_cardapio, obter_item_por_codigo, obter_item_por_id


def setup_module() -> None:
    """Prepara o banco de dados antes da execução dos testes."""
    inicializar_banco_dados()


def test_listar_cardapio_completo() -> None:
    """Verifica se a listagem de pratos e bebidas retorna dados."""
    itens = listar_cardapio()
    assert len(itens) >= 5


def test_obter_item_codigo_valido() -> None:
    """Testa a busca por código de item existente."""
    item = obter_item_por_codigo("RIS-01")
    assert item is not None
    assert item.nome == "Risoto de Funghi"
    assert item.preco > 0


def test_obter_item_codigo_inexistente() -> None:
    """Verifica que código desconhecido retorna None."""
    item = obter_item_por_codigo("NAO-EXISTE")
    assert item is None


def test_obter_item_por_id_valido() -> None:
    """Valida busca por identificador primário."""
    item = obter_item_por_id(1)
    assert item is not None
    assert item.codigo != ""
