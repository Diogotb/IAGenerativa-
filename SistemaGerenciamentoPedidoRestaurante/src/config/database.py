"""Módulo de conexão e configuração do banco de dados SQLite."""

import os
import sqlite3
from pathlib import Path


def carregar_variaveis_ambiente() -> None:
    """Carrega variáveis do arquivo .env caso existam sem sobrescrever o SO."""
    caminho_env = Path(".env")
    if not caminho_env.exists():
        return
    with open(caminho_env, "r", encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            if linha and not linha.startswith("#") and "=" in linha:
                chave, valor = linha.split("=", 1)
                os.environ.setdefault(chave.strip(), valor.strip())


def obter_caminho_banco() -> Path:
    """Retorna o caminho configurado do banco SQLite local."""
    carregar_variaveis_ambiente()
    caminho = os.getenv("DB_PATH", "src/database/restaurante.sqlite")
    if caminho.startswith("sqlite:///"):
        caminho = caminho.replace("sqlite:///", "")
    return Path(caminho)


def obter_conexao() -> sqlite3.Connection:
    """Cria e retorna uma conexão configurada com o SQLite."""
    caminho_banco = obter_caminho_banco()
    caminho_banco.parent.mkdir(parents=True, exist_ok=True)
    conexao = sqlite3.connect(str(caminho_banco))
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON;")
    return conexao


def inicializar_banco_dados() -> None:
    """Aplica o esquema DDL e os dados sementes no banco de dados."""
    caminho_schema = Path(__file__).parent / "schema.sql"
    caminho_seeds = Path(__file__).parent / "seeds.sql"
    with obter_conexao() as conexao:
        if caminho_schema.exists():
            with open(caminho_schema, "r", encoding="utf-8") as f:
                conexao.executescript(f.read())
        if caminho_seeds.exists():
            with open(caminho_seeds, "r", encoding="utf-8") as f:
                conexao.executescript(f.read())
        conexao.commit()
