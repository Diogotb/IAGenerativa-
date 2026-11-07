"""Tela de visualização de logs de auditoria e governança do sistema."""

import streamlit as st
from src.services.auditoria_service import ler_logs_auditoria


def renderizar_lista_logs(logs) -> None:
    """Renderiza os blocos de registro de auditoria em cartões legíveis."""
    st.write(f"Exibindo os últimos **{len(logs)}** eventos registrados:")
    for bloco in reversed(logs):
        with st.container(border=True):
            st.code(bloco, language="yaml")


def renderizar_auditoria() -> None:
    """Ponto de entrada para renderização da aba Auditoria."""
    st.header("Auditoria e Rastreabilidade do Sistema")
    st.caption("Logs gerados por agentes, skills e operações humanas com política Human-in-the-Loop.")
    if st.button("Atualizar Logs"):
        st.rerun()
    logs = ler_logs_auditoria(limite=30)
    if not logs:
        st.info("Nenhum registro de auditoria encontrado em '.antigravity/logs/audit.log'.")
        return
    renderizar_lista_logs(logs)
