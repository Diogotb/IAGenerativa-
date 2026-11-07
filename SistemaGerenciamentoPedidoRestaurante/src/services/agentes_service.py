"""Serviço de orquestração e execução de agentes Antigravity ou fallback local."""

import os
from typing import Any, Dict
from src.services import pedido_service, mesa_service, cardapio_service, auditoria_service


def mcp_disponivel() -> bool:
    """Verifica se há um servidor MCP ou daemon do Antigravity ativo."""
    return os.getenv("ANTIGRAVITY_MCP_ACTIVE", "false").lower() == "true"


def maitre_abrir_pedido(mesa: int, item: str, qtd: int, obs: str = "") -> Dict[str, Any]:
    """Aciona a recepção de pedido pelo Agente Maitre ou fallback de serviço local."""
    mcp_on = mcp_disponivel()
    origem = "Agente Maitre (MCP)" if mcp_on else "Serviço Local GastroFlow (MCP Offline)"
    sucesso, msg, pid = pedido_service.criar_pedido_com_item(mesa, item, qtd, obs)
    if sucesso:
        auditoria_service.registrar_auditoria(origem, "database_write", f"Abertura de pedido #{pid} na Mesa {mesa}")
    return {"sucesso": sucesso, "mensagem": msg, "pedido_id": pid, "origem": origem, "mcp_ativo": mcp_on}


def chef_atualizar_pedido(pedido_id: int, novo_status: str) -> Dict[str, Any]:
    """Aciona a gestão da cozinha pelo Agente Chef ou fallback de serviço local."""
    mcp_on = mcp_disponivel()
    origem = "Agente Chef (MCP)" if mcp_on else "Serviço Local GastroFlow (MCP Offline)"
    sucesso, msg = pedido_service.atualizar_status_pedido(pedido_id, novo_status)
    if sucesso:
        auditoria_service.registrar_auditoria(origem, "database_write", f"Atualização Pedido #{pedido_id} -> {novo_status}")
    return {"sucesso": sucesso, "mensagem": msg, "origem": origem, "mcp_ativo": mcp_on}


def chef_consultar_fila() -> Dict[str, Any]:
    """Consulta os pedidos em fila de produção da cozinha."""
    mcp_on = mcp_disponivel()
    origem = "Agente Chef (MCP)" if mcp_on else "Serviço Local GastroFlow (MCP Offline)"
    pedidos = pedido_service.listar_pedidos(apenas_ativos=True)
    fila = [p for p in pedidos if p.status in ("RECEBIDO", "PREPARANDO")]
    return {"origem": origem, "pedidos": fila, "mcp_ativo": mcp_on}


def caixa_fechar_conta(pedido_id: int, mesa: int, com_taxa: bool = True) -> Dict[str, Any]:
    """Aciona o fechamento e liquidação pelo Agente Caixa ou fallback de serviço local."""
    mcp_on = mcp_disponivel()
    origem = "Agente Caixa (MCP)" if mcp_on else "Serviço Local GastroFlow (MCP Offline)"
    sucesso, msg, total = pedido_service.liquidar_conta_mesa(pedido_id, mesa, com_taxa)
    if sucesso:
        auditoria_service.registrar_auditoria(origem, "database_write", f"Liquidação Pedido #{pedido_id} (R$ {total:.2f}) - Mesa {mesa} LIVRE")
    return {"sucesso": sucesso, "mensagem": msg, "valor_final": total, "origem": origem, "mcp_ativo": mcp_on}
