"""Tela de fechamento de conta, cálculo discriminado e liquidação."""

import streamlit as st
from src.services.pedido_service import (
    listar_pedidos,
    obter_pedido_ativo_mesa,
    liquidar_conta_mesa,
)
from src.services.mesa_service import listar_mesas


def renderizar_detalhes_fechamento(pedido, mesa_num: int) -> None:
    """Exibe o demonstrativo detalhado de consumo da mesa selecionada."""
    st.markdown(f"#### Memória de Cálculo — Comanda #{pedido.id} (Mesa {mesa_num})")
    for item in pedido.itens:
        st.write(f"- **{item.quantidade}x {item.nome_item}** ({item.codigo_item}): R$ {item.subtotal():.2f}")
    subtotal = pedido.valor_total
    aplicar_taxa = st.checkbox("Incluir taxa de serviço opcional (10%)", value=True)
    taxa = (subtotal * 0.10) if aplicar_taxa else 0.0
    total = subtotal + taxa
    st.markdown("---")
    c1, c2 = st.columns(2)
    c1.metric("Subtotal dos Itens", f"R$ {subtotal:.2f}")
    c2.metric("Total Final com Serviço", f"R$ {total:.2f}", delta=f"+ R$ {taxa:.2f}" if taxa else None)
    renderizar_confirmacao_liquidacao(pedido.id, mesa_num, total, aplicar_taxa)


def renderizar_confirmacao_liquidacao(pedido_id: int, mesa_num: int, total: float, taxa: bool) -> None:
    """Apresenta a confirmação de Human-in-the-Loop antes de liquidar o pedido."""
    with st.form("form_liquidar"):
        st.warning(f"Atenção: A liquidação alterará o pedido #{pedido_id} para 'PAGO' e liberará a Mesa {mesa_num}.")
        confirmar = st.checkbox(f"Confirmo o recebimento de R$ {total:.2f} e a liberação da mesa")
        if st.form_submit_button("Confirmar Pagamento e Liberar Mesa"):
            if not confirmar:
                st.error("É necessária autorização explícita antes de efetivar a liquidação.")
                return
            ok, msg, _ = liquidar_conta_mesa(pedido_id, mesa_num, taxa)
            (st.success if ok else st.error)(msg)
            if ok:
                st.rerun()


def renderizar_caixa() -> None:
    """Ponto de entrada para renderização da aba Caixa."""
    st.header("Fechamento de Contas e Caixa")
    mesas_ocupadas = [m for m in listar_mesas() if m.status == "OCUPADA"]
    if not mesas_ocupadas:
        st.info("Nenhuma mesa ocupada necessitando fechamento de conta no momento.")
        return
    mesa_sel = st.selectbox("Selecione a Mesa para Fechamento", [m.numero for m in mesas_ocupadas])
    pedido = obter_pedido_ativo_mesa(mesa_sel)
    if not pedido:
        st.warning(f"Nenhum pedido ativo encontrado para a Mesa {mesa_sel}.")
        return
    renderizar_detalhes_fechamento(pedido, mesa_sel)
