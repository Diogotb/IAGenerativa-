"""Tela de monitoramento e alteração manual do status das mesas."""

import streamlit as st
from src.services.mesa_service import listar_mesas, atualizar_status_mesa


def renderizar_acoes_mesa(mesa) -> None:
    """Renderiza os botões de ação rápida para alteração de status da mesa."""
    opcoes = [s for s in ("LIVRE", "OCUPADA", "RESERVADA") if s != mesa.status]
    cols = st.columns(len(opcoes))
    for idx, novo_status in enumerate(opcoes):
        if cols[idx].button(f"Mudar para {novo_status}", key=f"btn_m_{mesa.numero}_{novo_status}"):
            if atualizar_status_mesa(mesa.numero, novo_status):
                st.success(f"Mesa {mesa.numero} atualizada para {novo_status}!")
                st.rerun()


def renderizar_grade_mesas(mesas) -> None:
    """Renderiza as mesas em layout de grade responsiva."""
    cols = st.columns(3)
    cores = {"LIVRE": "🟢", "OCUPADA": "🔴", "RESERVADA": "🟡"}
    for idx, mesa in enumerate(mesas):
        with cols[idx % 3]:
            with st.container(border=True):
                st.markdown(f"### {cores.get(mesa.status, '⚪')} Mesa {mesa.numero}")
                st.caption(f"Capacidade: {mesa.capacidade} pessoas | Status: **{mesa.status}**")
                renderizar_acoes_mesa(mesa)


def renderizar_mesas() -> None:
    """Ponto de entrada para renderização da aba de Mesas."""
    st.header("Gestão de Mesas do Salão")
    mesas = listar_mesas()
    if not mesas:
        st.warning("Nenhuma mesa configurada no banco de dados.")
        return
    renderizar_grade_mesas(mesas)
