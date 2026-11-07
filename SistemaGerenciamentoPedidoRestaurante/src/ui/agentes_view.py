"""Tela de interação com os Agentes Antigravity (@Maitre, @Chef, @Caixa)."""

import streamlit as st
from src.services.agentes_service import (
    mcp_disponivel,
    maitre_abrir_pedido,
    chef_consultar_fila,
    chef_atualizar_pedido,
    caixa_fechar_conta,
)
from src.services.mesa_service import listar_mesas, obter_mesa_por_numero
from src.services.cardapio_service import listar_cardapio
from src.services.pedido_service import listar_pedidos, obter_pedido_ativo_mesa


def renderizar_banner_status_mcp() -> None:
    """Exibe o status de conectividade do MCP do Google Antigravity."""
    ativo = mcp_disponivel()
    if ativo:
        st.success("🟢 Integração MCP Antigravity: CONECTADA (Agentes operando via protocolo)")
    else:
        st.info(
            "ℹ️ Integração MCP Antigravity: NÃO DISPONÍVEL (Operação local equivalente via GastroFlow Service ativada. Nenhuma simulação falsa é executada)."
        )


def renderizar_painel_maitre() -> None:
    """Painel de acionamento do @AgenteMaitre com validação prévia."""
    st.subheader("🎩 @AgenteMaitre — Recepção e Validação")
    st.caption("Verifica mesas no banco, checa disponibilidade no cardápio e abre pedidos.")
    mesas = listar_mesas()
    itens = listar_cardapio(apenas_disponiveis=True)
    c1, c2, c3 = st.columns(3)
    mesa_sel = c1.selectbox("Mesa", [m.numero for m in mesas], key="agt_m_mesa")
    item_sel = c2.selectbox("Item Cardápio", [f"{i.codigo} - {i.nome}" for i in itens], key="agt_m_item")
    qtd = c3.number_input("Qtd", min_value=1, value=1, key="agt_m_qtd")
    obs = st.text_input("Observação Alimentar", key="agt_m_obs")
    confirmar = st.checkbox("Autorizo a gravação do pedido", key="agt_m_conf")
    if st.button("Disparar Abertura via Maitre"):
        if not confirmar:
            st.error("Confirmação humana explícita obrigatória antes da gravação.")
            return
        cod = item_sel.split(" - ")[0]
        res = maitre_abrir_pedido(mesa_sel, cod, qtd, obs)
        st.write(f"**Origem da Execução:** `{res['origem']}`")
        (st.success if res["sucesso"] else st.error)(res["mensagem"])


def renderizar_painel_chef() -> None:
    """Painel de acionamento do @AgenteChef para controle da linha de produção."""
    st.subheader("👨‍🍳 @AgenteChef — Fila de Cozinha e KDS")
    res_fila = chef_consultar_fila()
    st.write(f"**Canal de Consulta:** `{res_fila['origem']}`")
    fila = res_fila["pedidos"]
    if not fila:
        st.info("Nenhum pedido pendente de preparação na cozinha.")
        return
    for p in fila:
        with st.container(border=True):
            st.markdown(f"**Comanda #{p.id} — Mesa {p.mesa_numero}** | Status: `{p.status}`")
            for i in p.itens:
                obs = f" - *{i.observacao}*" if i.observacao else ""
                st.text(f"• {i.quantidade}x {i.nome_item}{obs}")
            c1, c2 = st.columns(2)
            if p.status == "RECEBIDO" and c1.button("Iniciar Preparo (PREPARANDO)", key=f"chef_prep_{p.id}"):
                res = chef_atualizar_pedido(p.id, "PREPARANDO")
                st.success(res["mensagem"])
                st.rerun()
            if p.status == "PREPARANDO" and c2.button("Concluir Preparo (PRONTO)", key=f"chef_pronto_{p.id}"):
                res = chef_atualizar_pedido(p.id, "PRONTO")
                st.success(res["mensagem"])
                st.rerun()


def renderizar_painel_caixa() -> None:
    """Painel de acionamento do @AgenteCaixa para apuração e encerramento."""
    st.subheader("💳 @AgenteCaixa — Fechamento Financeiro")
    ocupadas = [m.numero for m in listar_mesas() if m.status == "OCUPADA"]
    if not ocupadas:
        st.info("Nenhuma mesa aberta para fechamento.")
        return
    mesa_sel = st.selectbox("Mesa a Liquidar", ocupadas, key="agt_cx_mesa")
    ped = obter_pedido_ativo_mesa(mesa_sel)
    if not ped:
        st.warning("Comanda não localizada.")
        return
    st.write(f"Total dos itens consumidos: **R$ {ped.valor_total:.2f}**")
    taxa = st.checkbox("Aplicar 10% de serviço", value=True, key="agt_cx_taxa")
    conf = st.checkbox("Confirmo o recebimento financeiro", key="agt_cx_conf")
    if st.button("Fechar e Liquidar via Caixa"):
        if not conf:
            st.error("Aprovação humana mandatória antes da liquidação.")
            return
        res = caixa_fechar_conta(ped.id, mesa_sel, taxa)
        st.write(f"**Origem da Execução:** `{res['origem']}`")
        st.success(res["mensagem"])
        st.rerun()


def renderizar_agentes() -> None:
    """Ponto de entrada para renderização da aba Agentes."""
    st.header("Ecossistema de Agentes Antigravity")
    renderizar_banner_status_mcp()
    st.divider()
    aba_m, aba_c, aba_cx = st.tabs(["@AgenteMaitre", "@AgenteChef", "@AgenteCaixa"])
    with aba_m:
        renderizar_painel_maitre()
    with aba_c:
        renderizar_painel_chef()
    with aba_cx:
        renderizar_painel_caixa()
