"""Tela de visualização de pratos e bebidas do cardápio."""

import streamlit as st
from src.services.cardapio_service import listar_cardapio


def renderizar_tabela_cardapio(itens) -> None:
    """Monta a tabela estruturada com os itens do menu."""
    dados = [
        {
            "Código": item.codigo,
            "Nome": item.nome,
            "Categoria": item.categoria,
            "Preço": item.preco_formatado(),
            "Disponibilidade": "Disponível" if item.disponivel else "Esgotado",
        }
        for item in itens
    ]
    st.dataframe(dados, use_container_width=True)


def renderizar_cardapio() -> None:
    """Ponto de entrada para renderização da aba Cardápio."""
    st.header("Cardápio do GastroFlow")
    apenas_disponiveis = st.checkbox("Exibir somente itens disponíveis", value=False)
    itens = listar_cardapio(apenas_disponiveis=apenas_disponiveis)
    if not itens:
        st.info("Nenhum item cadastrado no cardápio.")
        return
    renderizar_tabela_cardapio(itens)
