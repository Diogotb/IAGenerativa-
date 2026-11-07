"""Testes unitários para o serviço de mesas."""

from src.config.database import inicializar_banco_dados
from src.services.mesa_service import listar_mesas, obter_mesa_por_numero, atualizar_status_mesa


def setup_module() -> None:
    """Prepara o banco de dados antes da execução dos testes."""
    inicializar_banco_dados()


def test_listar_mesas_retorna_lista() -> None:
    """Verifica se a listagem de mesas retorna registros válidos."""
    mesas = listar_mesas()
    assert len(mesas) > 0
    assert hasattr(mesas[0], "numero")


def test_obter_mesa_existente() -> None:
    """Valida a recuperação de uma mesa específica pelo número."""
    mesa = obter_mesa_por_numero(1)
    assert mesa is not None
    assert mesa.numero == 1


def test_obter_mesa_inexistente() -> None:
    """Verifica que a busca por número inválido retorna None."""
    mesa = obter_mesa_por_numero(9999)
    assert mesa is None


def test_atualizar_status_mesa_valido() -> None:
    """Testa a alteração de status para um valor aceito."""
    sucesso = atualizar_status_mesa(1, "RESERVADA")
    assert sucesso is True
    mesa = obter_mesa_por_numero(1)
    assert mesa.status == "RESERVADA"
    atualizar_status_mesa(1, "LIVRE")


def test_atualizar_status_mesa_invalido() -> None:
    """Impede que status desconhecido seja aceito pelo serviço."""
    sucesso = atualizar_status_mesa(1, "STATUS_INVENTADO")
    assert sucesso is False
