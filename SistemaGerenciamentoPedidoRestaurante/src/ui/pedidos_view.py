"""Tela de abertura, adição de itens e acompanhamento de pedidos."""

import streamlit as st
from src.services.cardapio_service import listar_cardapio, obter_item_por_codigo
from src.services.mesa_service import listar_mesas
from src.services.pedido_service import (
    listar_pedidos,
    criar_pedido_com_item,
    adicionar_item_a_pedido,
    atualizar_status_pedido,
)


def renderizar_form_abertura(mesas, itens) -> None:
    """Renderiza o formulário de abertura de pedido com confirmação prévia."""
    st.subheader("Abrir Novo Pedido")
    with st.form("form_abrir_pedido"):
        m_opts = [m.numero for m in mesas]
        c_opts = [f"{i.codigo} - {i.nome} ({i.preco_formatado()})" for i in itens if i.disponivel]
        mesa_sel = st.selectbox("Selecione a Mesa", m_opts)
        item_sel = st.selectbox("Selecione o Item", c_opts)
        qtd = st.number_input("Quantidade", min_value=1, max_value=20, value=1)
        obs = st.text_input("Observações (ex: sem cebola, gelo à parte)")
        confirmar = st.checkbox("Confirmo a abertura do pedido no banco de dados")
        enviado = st.form_submit_button("Abrir Pedido")
        if enviado:
            if not confirmar:
                st.error("É obrigatório marcar a confirmação explícita antes de gravar.")
                return
            cod = item_sel.split(" - ")[0]
            ok, msg, _ = criar_pedido_com_item(mesa_sel, cod, qtd, obs)
            (st.success if ok else st.error)(msg)
            if ok:
                st.rerun()


def renderizar_form_adicionar_item(pedidos_ativos, itens) -> None:
    """Permite adicionar novos itens a um pedido ativo existente."""
    st.subheader("Adicionar Item a Pedido Ativo")
    if not pedidos_ativos:
        st.caption("Nenhum pedido em aberto disponível para adição.")
        return
    with st.form("form_add_item"):
        p_opts = [f"Pedido #{p.id} (Mesa {p.mesa_numero}) - {p.status}" for p in pedidos_ativos]
        c_opts = [f"{i.codigo} - {i.nome} ({i.preco_formatado()})" for i in itens if i.disponivel]
        ped_sel = st.selectbox("Pedido Alvo", p_opts)
        item_sel = st.selectbox("Item a Adicionar", c_opts)
        qtd = st.number_input("Quantidade Adicional", min_value=1, max_value=20, value=1)
        obs = st.text_input("Observação do Item Adicional")
        confirmar = st.checkbox("Confirmo a gravação deste item no pedido selecionado")
        if st.form_submit_button("Gravar Item"):
            if not confirmar:
                st.error("Confirmação humana obrigatória para inclusão de itens.")
                return
            pid = int(ped_sel.split(" ")[1].replace("#", ""))
            cod = item_sel.split(" - ")[0]
            ok, msg = adicionar_item_a_pedido(pid, cod, qtd, obs)
            (st.success if ok else st.error)(msg)
            if ok:
                st.rerun()


def renderizar_controles_status(pedido) -> None:
    """Renderiza os botões para avançar o ciclo de vida do pedido."""
    fluxo = {"RECEBIDO": "PREPARANDO", "PREPARANDO": "PRONTO", "PRONTO": "ENTREGUE"}
    proximo = fluxo.get(pedido.status)
    cols = st.columns(3)
    if proximo and cols[0].button(f"Mudar para {proximo}", key=f"btn_st_{pedido.id}_{proximo}"):
        atualizar_status_pedido(pedido.id, proximo)
        st.rerun()
    if pedido.status != "CANCELADO" and cols[1].button("Cancelar Pedido", key=f"btn_canc_{pedido.id}"):
        atualizar_status_pedido(pedido.id, "CANCELADO")
        st.rerun()


def renderizar_cartoes_pedidos_ativos(pedidos) -> None:
    """Renderiza a lista visual das comandas ativas no restaurante."""
    st.subheader("Acompanhamento de Comandas Ativas")
    ativos = [p for p in pedidos if p.em_aberto()]
    if not ativos:
        st.info("Nenhuma comanda ativa no momento.")
        return
    for p in ativos:
        with st.container(border=True):
            st.markdown(f"**Pedido #{p.id} — Mesa {p.mesa_numero}** | Status: `{p.status}` | Abertura: {p.data_hora}")
            st.markdown(f"**Total acumulado:** R$ {p.valor_total:.2f}")
            for item in p.itens:
                obs_txt = f" *({item.observacao})*" if item.observacao else ""
                st.text(f"• {item.quantidade}x {item.nome_item} - R$ {item.subtotal():.2f}{obs_txt}")
            renderizar_controles_status(p)


def renderizar_pedidos() -> None:
    """Ponto de entrada para renderização da aba Pedidos."""
    st.header("Gerenciamento de Pedidos e Cozinha")
    mesas = listar_mesas()
    itens = listar_cardapio(apenas_disponiveis=True)
    pedidos = listar_pedidos()
    aba_abrir, aba_add, aba_lista = st.tabs(["Abrir Pedido", "Adicionar Itens", "Acompanhar"])
    with aba_abrir:
        renderizar_form_abertura(mesas, itens)
    with aba_add:
        renderizar_form_adicionar_item([p for p in pedidos if p.em_aberto()], itens)
    with aba_lista:
        renderizar_cartoes_pedidos_ativos(pedidos)
