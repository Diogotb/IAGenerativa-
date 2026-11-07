"""Serviço de disparo e execução das skills do Antigravity com fallback seguro."""

import ast
import io
import sys
from pathlib import Path
from typing import Any, Dict, List
import pytest
from src.services import pedido_service, auditoria_service


def skill_abrir_pedido(mesa: int, codigo: str, qtd: int, obs: str = "") -> Dict[str, Any]:
    """Executa a skill /abrir-pedido de forma transacional e auditada."""
    sucesso, msg, pid = pedido_service.criar_pedido_com_item(mesa, codigo, qtd, obs)
    if sucesso:
        auditoria_service.registrar_auditoria("Skill /abrir-pedido", "database_write", f"Pedido #{pid} na Mesa {mesa}")
    return {"sucesso": sucesso, "mensagem": msg, "pedido_id": pid}


def listar_testes_previstos() -> List[str]:
    """Mapeia os nomes das funções de teste definidas no diretório tests/."""
    pasta_testes = Path("tests")
    testes_encontrados = []
    if not pasta_testes.exists():
        return testes_encontrados
    for arq in pasta_testes.glob("test_*.py"):
        try:
            with open(arq, "r", encoding="utf-8") as f:
                arvore = ast.parse(f.read(), filename=str(arq))
            for item in ast.walk(arvore):
                if isinstance(item, ast.FunctionDef) and item.name.startswith("test_"):
                    testes_encontrados.append(f"{arq.name}::{item.name}")
        except Exception:
            continue
    return testes_encontrados


def executar_testes_pytest() -> Dict[str, Any]:
    """Executa a suíte de testes com pytest capturando a saída de forma segura."""
    buffer_saida = io.StringIO()
    stdout_original = sys.stdout
    sys.stdout = buffer_saida
    try:
        codigo_retorno = pytest.main(["-v", "tests"])
    finally:
        sys.stdout = stdout_original
    saida = buffer_saida.getvalue()
    auditoria_service.registrar_auditoria("Skill /test", "terminal_execute", f"pytest finalizado com código {codigo_retorno}")
    return {"sucesso": codigo_retorno == 0, "codigo_retorno": codigo_retorno, "saida": saida}


def skill_auditoria_seguranca() -> Dict[str, Any]:
    """Executa a skill /audit-security sem vazar valores de segredos."""
    resultado = auditoria_service.executar_auditoria_seguranca("src")
    auditoria_service.registrar_auditoria("Skill /audit-security", "filesystem_read", "Auditoria de segurança em /src concluída")
    return resultado
