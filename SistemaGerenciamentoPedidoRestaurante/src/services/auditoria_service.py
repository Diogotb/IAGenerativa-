"""Serviço de auditoria de operações, conformidade de código e segurança."""

import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List


def registrar_auditoria(agente: str, acao: str, detalhes: str) -> None:
    """Registra uma entrada padronizada no arquivo de log de auditoria."""
    caminho_log = Path(".antigravity/logs/audit.log")
    caminho_log.parent.mkdir(parents=True, exist_ok=True)
    agora = datetime.now().isoformat()
    entrada = (
        f"[{agora}] [AUDIT] [AGENTE: {agente}] [ACAO: {acao}]\n"
        f"Detalhes: {detalhes}\n"
        "--------------------------------------------------------------------------------\n"
    )
    with open(caminho_log, "a", encoding="utf-8") as f:
        f.write(entrada)


def ler_logs_auditoria(limite: int = 50) -> List[str]:
    """Lê as entradas recentes do arquivo de log de auditoria."""
    caminho_log = Path(".antigravity/logs/audit.log")
    if not caminho_log.exists():
        return []
    with open(caminho_log, "r", encoding="utf-8") as f:
        linhas = f.readlines()
    blocos = "".join(linhas).split("--------------------------------------------------------------------------------\n")
    return [b.strip() for b in blocos if b.strip()][-limite:]


def checar_funcoes_longas(conteudo: str, nome_arq: str) -> List[Dict[str, any]]:
    """Identifica funções que ultrapassam o teto de 20 linhas."""
    linhas = conteudo.splitlines()
    achados, def_atual, inicio = [], None, 0
    for idx, lin in enumerate(linhas, start=1):
        if lin.strip().startswith("def "):
            if def_atual and (idx - inicio) > 20:
                achados.append({"arquivo": nome_arq, "linha": inicio, "item": def_atual, "violacao": f"Função com {idx - inicio} linhas (>20)"})
            def_atual = lin.strip().split("(")[0].replace("def ", "")
            inicio = idx
    if def_atual and (len(linhas) - inicio + 1) > 20:
        achados.append({"arquivo": nome_arq, "linha": inicio, "item": def_atual, "violacao": f"Função com {len(linhas) - inicio + 1} linhas (>20)"})
    return achados


def checar_segredos(conteudo: str, nome_arq: str) -> List[Dict[str, any]]:
    """Detecta potenciais segredos ou credenciais atribuídos diretamente no código."""
    padrao = re.compile(r"(password|senha|secret|api_key|token)\s*=\s*['\"][^'\"]{4,}['\"]", re.IGNORECASE)
    achados = []
    for idx, lin in enumerate(conteudo.splitlines(), start=1):
        if padrao.search(lin) and "os.getenv" not in lin:
            achados.append({"arquivo": nome_arq, "linha": idx, "violacao": "Possível segredo ou credencial estática (hardcoded)"})
    return achados


def checar_sql_inseguro(conteudo: str, nome_arq: str) -> List[Dict[str, any]]:
    """Localiza interpolações de strings em comandos de banco de dados."""
    achados = []
    for idx, lin in enumerate(conteudo.splitlines(), start=1):
        if ("execute(" in lin or "executescript(" in lin) and ("f\"" in lin or "f'" in lin or "%" in lin or " + " in lin):
            achados.append({"arquivo": nome_arq, "linha": idx, "violacao": "Consulta SQL construída com interpolação (risco de SQL Injection)"})
    return achados


def executar_auditoria_seguranca(diretorio: str = "src") -> Dict[str, any]:
    """Varre arquivos de código do diretório reportando violações de qualidade e segurança."""
    pasta = Path(diretorio)
    resultado = {"total_arquivos": 0, "funcoes_longas": [], "segredos": [], "sql_inseguro": []}
    if not pasta.exists():
        return resultado
    for arq in pasta.rglob("*.py"):
        resultado["total_arquivos"] += 1
        with open(arq, "r", encoding="utf-8") as f:
            texto = f.read()
        rel = str(arq.relative_to(pasta.parent))
        resultado["funcoes_longas"].extend(checar_funcoes_longas(texto, rel))
        resultado["segredos"].extend(checar_segredos(texto, rel))
        resultado["sql_inseguro"].extend(checar_sql_inseguro(texto, rel))
    return resultado
