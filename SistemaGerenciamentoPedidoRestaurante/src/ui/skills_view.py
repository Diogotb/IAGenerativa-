"""Tela de execução das Skills Antigravity (/abrir-pedido, /test, /audit-security)."""

import streamlit as st
from src.services.skills_service import (
    skill_abrir_pedido,
    listar_testes_previstos,
    executar_testes_pytest,
    skill_auditoria_seguranca,
)
from src.services.mesa_service import listar_mesas
from src.services.cardapio_service import listar_cardapio


def renderizar_skill_abrir_pedido() -> None:
    """Interface para disparo da skill /abrir-pedido com parâmetros validados."""
    st.subheader("⚡ Skill `/abrir-pedido`")
    mesas = listar_mesas()
    itens = listar_cardapio(apenas_disponiveis=True)
    c1, c2 = st.columns(2)
    mesa_sel = c1.selectbox("Mesa Alvo", [m.numero for m in mesas], key="sk_mesa")
    item_sel = c2.selectbox("Código / Item", [f"{i.codigo} - {i.nome}" for i in itens], key="sk_item")
    qtd = st.number_input("Quantidade", min_value=1, value=1, key="sk_qtd")
    obs = st.text_input("Observações", key="sk_obs")
    conf = st.checkbox("Confirmo gravação dos dados via Skill", key="sk_abrir_conf")
    if st.button("Executar /abrir-pedido"):
        if not conf:
            st.error("Confirmação humana explícita obrigatória.")
            return
        cod = item_sel.split(" - ")[0]
        res = skill_abrir_pedido(mesa_sel, cod, qtd, obs)
        (st.success if res["sucesso"] else st.error)(res["mensagem"])


def renderizar_skill_test() -> None:
    """Interface para a skill /test com exibição prévia da suíte e confirmação."""
    st.subheader("🧪 Skill `/test` (pytest)")
    testes = listar_testes_previstos()
    st.markdown("**Testes Automatizados Mapeados:**")
    for t in testes:
        st.write(f"- `{t}`")
    st.info("Comando seguro pré-configurado: `pytest -v tests` (Comandos externos do usuário são bloqueados).")
    conf = st.checkbox("Autorizo formalmente a execução dos testes no ambiente", key="sk_test_conf")
    if st.button("Executar Suíte de Testes"):
        if not conf:
            st.error("É necessário confirmar a execução da suíte de testes.")
            return
        with st.spinner("Executando pytest..."):
            res = executar_testes_pytest()
        if res["sucesso"]:
            st.success("Todos os testes passaram com sucesso!")
        else:
            st.warning("A suíte rodou com apontamentos ou falhas.")
        st.code(res["saida"], language="text")


def renderizar_skill_audit() -> None:
    """Interface para a skill /audit-security sem exposição de segredos."""
    st.subheader("🛡️ Skill `/audit-security`")
    st.caption("Varre o diretório /src buscando senhas hardcoded, queries inseguras e funções >20 linhas.")
    if st.button("Executar Auditoria de Segurança"):
        with st.spinner("Analisando código-fonte..."):
            res = skill_auditoria_seguranca()
        st.metric("Total de Arquivos Analisados", res["total_arquivos"])
        st.write("#### 1. Potenciais Segredos / Credenciais Estáticas")
        st.caption("Valores confidenciais são mascarados por segurança.")
        if not res["segredos"]:
            st.success("Nenhum segredo estático detectado.")
        else:
            st.error(f"{len(res['segredos'])} apontamento(s) de credenciais fixas:")
            for s in res["segredos"]:
                st.write(f"- `{s['arquivo']}` (linha {s['linha']}): {s['violacao']}")
        st.write("#### 2. Consultas sem Parametrização (?)")
        if not res["sql_inseguro"]:
            st.success("Todas as consultas analisadas utilizam parâmetros seguros.")
        else:
            st.warning(f"{len(res['sql_inseguro'])} consulta(s) com risco de injeção:")
            for q in res["sql_inseguro"]:
                st.write(f"- `{q['arquivo']}` (linha {q['linha']}): {q['violacao']}")
        st.write("#### 3. Funções com Mais de 20 Linhas (SOLID / Clean Code)")
        if not res["funcoes_longas"]:
            st.success("Todas as funções respeitam o limite máximo de 20 linhas.")
        else:
            st.warning(f"{len(res['funcoes_longas'])} função(ões) longa(s) detectada(s):")
            for f in res["funcoes_longas"]:
                st.write(f"- `{f['arquivo']}` (linha {f['linha']}) -> `{f['item']}`: {f['violacao']}")


def renderizar_skills() -> None:
    """Ponto de entrada para renderização da aba Skills."""
    st.header("Catálogo de Skills Operacionais")
    aba1, aba2, aba3 = st.tabs(["/abrir-pedido", "/test", "/audit-security"])
    with aba1:
        renderizar_skill_abrir_pedido()
    with aba2:
        renderizar_skill_test()
    with aba3:
        renderizar_skill_audit()
