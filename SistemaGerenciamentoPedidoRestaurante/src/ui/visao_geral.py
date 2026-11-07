"""Tela de visão geral e métricas operacionais do restaurante."""

import streamlit as st
from src.services.mesa_service import listar_mesas
from src.services.pedido_service import listar_pedidos


def renderizar_metricas(mesas, pedidos) -> None:
    """Renderiza os cartões de métricas rápidas no topo do painel."""
    livres = sum(1 for m in mesas if m.status == "LIVRE")
    ocupadas = sum(1 for m in mesas if m.status == "OCUPADA")
    ativos = sum(1 for p in pedidos if p.em_aberto())
    total_faturado = sum(p.valor_total for p in pedidos if p.status == "PAGO")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Mesas Livres", f"{livres}/{len(mesas)}")
    c2.metric("Mesas Ocupadas", ocupadas)
    c3.metric("Pedidos em Aberto", ativos)
    c4.metric("Faturamento Líquido", f"R$ {total_faturado:.2f}")


def renderizar_lista_pedidos_recentes(pedidos) -> None:
    """Exibe tabela com os pedidos mais recentes e seus status."""
    st.subheader("Últimos Pedidos")
    if not pedidos:
        st.info("Nenhum pedido registrado até o momento.")
        return
    dados = [
        {"ID": p.id, "Mesa": p.mesa_numero, "Horário": p.data_hora, "Status": p.status, "Total": f"R$ {p.valor_total:.2f}"}
        for p in pedidos[:10]
    ]
    st.dataframe(dados, use_container_width=True)


def renderizar_visao_geral() -> None:
    """Ponto de entrada para renderização da aba Visão Geral."""
    st.header("Visão Geral do Restaurante")
    mesas = listar_mesas()
    pedidos = listar_pedidos()
    renderizar_metricas(mesas, pedidos)
    st.divider()
    renderizar_lista_pedidos_recentes(pedidos)
