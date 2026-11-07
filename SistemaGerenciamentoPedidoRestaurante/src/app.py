"""Aplicação principal Streamlit do sistema GastroFlow."""

import streamlit as st
from src.config.database import inicializar_banco_dados
from src.ui.visao_geral import renderizar_visao_geral
from src.ui.mesas_view import renderizar_mesas
from src.ui.cardapio_view import renderizar_cardapio
from src.ui.pedidos_view import renderizar_pedidos
from src.ui.caixa_view import renderizar_caixa
from src.ui.agentes_view import renderizar_agentes
from src.ui.skills_view import renderizar_skills
from src.ui.auditoria_view import renderizar_auditoria


def configurar_pagina() -> None:
    """Configura o layout e título inicial da aplicação no Streamlit."""
    st.set_page_config(
        page_title="GastroFlow - Gestão Inteligente de Restaurante",
        page_icon="🍽️",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def renderizar_navegacao_lateral() -> str:
    """Monta o menu de navegação responsivo na barra lateral."""
    st.sidebar.title("🍽️ GastroFlow")
    st.sidebar.caption("Gestão de Pedidos, Mesas e Cozinha")
    opcoes = [
        "📊 Visão Geral",
        "🪑 Mesas",
        "📋 Cardápio",
        "🛎️ Pedidos",
        "💳 Caixa & Fechamento",
        "🤖 Agentes",
        "⚡ Skills",
        "🛡️ Auditoria",
    ]
    return st.sidebar.radio("Navegação Principal", opcoes)


def rotear_tela(opcao_selecionada: str) -> None:
    """Direciona a renderização para a visualização selecionada."""
    mapa_telas = {
        "📊 Visão Geral": renderizar_visao_geral,
        "🪑 Mesas": renderizar_mesas,
        "📋 Cardápio": renderizar_cardapio,
        "🛎️ Pedidos": renderizar_pedidos,
        "💳 Caixa & Fechamento": renderizar_caixa,
        "🤖 Agentes": renderizar_agentes,
        "⚡ Skills": renderizar_skills,
        "🛡️ Auditoria": renderizar_auditoria,
    }
    tela_func = mapa_telas.get(opcao_selecionada)
    if tela_func:
        tela_func()


def main() -> None:
    """Inicializa as dependências do banco e orquestra a interface."""
    configurar_pagina()
    inicializar_banco_dados()
    opcao = renderizar_navegacao_lateral()
    rotear_tela(opcao)


if __name__ == "__main__":
    main()
