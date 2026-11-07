"""Testes unitários para o serviço de auditoria e varredura de segurança."""

from src.services.auditoria_service import (
    registrar_auditoria,
    ler_logs_auditoria,
    executar_auditoria_seguranca,
)


def test_registrar_e_ler_auditoria() -> None:
    """Verifica se novos eventos de auditoria são persistidos e lidos."""
    registrar_auditoria("TesteUnitario", "acao_teste", "Validando escrita de log")
    logs = ler_logs_auditoria(limite=5)
    assert len(logs) > 0
    assert any("TesteUnitario" in l for l in logs)


def test_executar_auditoria_seguranca_estrutura() -> None:
    """Valida o formato e as chaves do dicionário retornado na varredura."""
    relatorio = executar_auditoria_seguranca("src")
    assert "total_arquivos" in relatorio
    assert "funcoes_longas" in relatorio
    assert "segredos" in relatorio
    assert "sql_inseguro" in relatorio
    assert relatorio["total_arquivos"] > 0
