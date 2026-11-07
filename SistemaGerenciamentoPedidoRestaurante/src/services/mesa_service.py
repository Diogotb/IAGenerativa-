"""Serviço de gerenciamento e consulta de mesas do restaurante."""

from typing import List, Optional
from src.config.database import obter_conexao
from src.models.mesa import Mesa


def mapear_linha_mesa(linha) -> Mesa:
    """Converte um registro do banco de dados na entidade Mesa."""
    return Mesa(
        id=linha["id"],
        numero=linha["numero"],
        capacidade=linha["capacidade"],
        status=linha["status"],
    )


def listar_mesas() -> List[Mesa]:
    """Retorna todas as mesas ordenadas pelo número."""
    with obter_conexao() as conexao:
        linhas = conexao.execute(
            "SELECT id, numero, capacidade, status FROM mesas ORDER BY numero;"
        ).fetchall()
        return [mapear_linha_mesa(linha) for linha in linhas]


def obter_mesa_por_numero(numero: int) -> Optional[Mesa]:
    """Busca uma mesa específica pelo seu número."""
    with obter_conexao() as conexao:
        linha = conexao.execute(
            "SELECT id, numero, capacidade, status FROM mesas WHERE numero = ?;",
            (numero,),
        ).fetchone()
        return mapear_linha_mesa(linha) if linha else None


def atualizar_status_mesa(numero: int, novo_status: str) -> bool:
    """Atualiza o status de atendimento da mesa no banco de dados."""
    status_validos = ("LIVRE", "OCUPADA", "RESERVADA")
    if novo_status not in status_validos:
        return False
    with obter_conexao() as conexao:
        cursor = conexao.execute(
            "UPDATE mesas SET status = ? WHERE numero = ?;",
            (novo_status, numero),
        )
        conexao.commit()
        return cursor.rowcount > 0
