"""Módulo para inicialização do banco de dados SQLite."""

import os
import sqlite3
from pathlib import Path


def carregar_script_sql(caminho_arquivo: Path) -> str:
    """Lê e retorna o conteúdo do arquivo de esquema SQL."""
    with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
        return arquivo.read()


def obter_caminho_banco() -> Path:
    """Retorna o caminho do banco configurado em variável ou o padrão."""
    caminho_env = os.getenv("DB_PATH", "restaurante.sqlite")
    if caminho_env.startswith("sqlite:///"):
        caminho_env = caminho_env.replace("sqlite:///", "")
    return Path(caminho_env)


def executar_esquema(caminho_banco: Path, script_sql: str) -> None:
    """Aplica o script SQL de criação no banco SQLite especificado."""
    with sqlite3.connect(caminho_banco) as conexao:
        conexao.executescript(script_sql)
        conexao.commit()


def inicializar_banco() -> Path:
    """Coordena a inicialização da estrutura do banco de dados."""
    caminho_schema = Path(__file__).parent / "schema.sql"
    caminho_banco = obter_caminho_banco()
    script = carregar_script_sql(caminho_schema)
    executar_esquema(caminho_banco, script)
    return caminho_banco


if __name__ == "__main__":
    banco = inicializar_banco()
    print(f"Banco de dados inicializado em: {banco}")
