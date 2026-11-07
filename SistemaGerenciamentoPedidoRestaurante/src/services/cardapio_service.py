"""Serviço de consulta e controle de pratos e bebidas do cardápio."""

from typing import List, Optional
from src.config.database import obter_conexao
from src.models.cardapio import ItemCardapio


def mapear_linha_cardapio(linha) -> ItemCardapio:
    """Converte um registro do banco de dados na entidade ItemCardapio."""
    return ItemCardapio(
        id=linha["id"],
        codigo=linha["codigo"],
        nome=linha["nome"],
        categoria=linha["categoria"],
        preco=float(linha["preco"]),
        disponivel=bool(linha["disponivel"]),
    )


def listar_cardapio(apenas_disponiveis: bool = False) -> List[ItemCardapio]:
    """Retorna itens do cardápio com opção de filtro por disponibilidade."""
    sql = "SELECT id, codigo, nome, categoria, preco, disponivel FROM cardapio"
    parametros = ()
    if apenas_disponiveis:
        sql += " WHERE disponivel = 1"
    sql += " ORDER BY categoria, nome;"
    with obter_conexao() as conexao:
        linhas = conexao.execute(sql, parametros).fetchall()
        return [mapear_linha_cardapio(linha) for linha in linhas]


def obter_item_por_codigo(codigo: str) -> Optional[ItemCardapio]:
    """Busca um item do cardápio pelo seu código único."""
    with obter_conexao() as conexao:
        linha = conexao.execute(
            "SELECT id, codigo, nome, categoria, preco, disponivel FROM cardapio WHERE codigo = ?;",
            (codigo.strip().upper(),),
        ).fetchone()
        return mapear_linha_cardapio(linha) if linha else None


def obter_item_por_id(item_id: int) -> Optional[ItemCardapio]:
    """Busca um item do cardápio pelo seu identificador primário."""
    with obter_conexao() as conexao:
        linha = conexao.execute(
            "SELECT id, codigo, nome, categoria, preco, disponivel FROM cardapio WHERE id = ?;",
            (item_id,),
        ).fetchone()
        return mapear_linha_cardapio(linha) if linha else None
