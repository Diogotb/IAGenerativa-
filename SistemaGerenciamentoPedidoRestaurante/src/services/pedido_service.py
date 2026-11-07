"""Serviço de gerenciamento do ciclo de vida de pedidos e comandas."""

from typing import List, Optional, Tuple
from src.config.database import obter_conexao
from src.models.pedido import Pedido
from src.models.item_pedido import ItemPedido
from src.services.cardapio_service import obter_item_por_codigo
from src.services.mesa_service import obter_mesa_por_numero, atualizar_status_mesa


def buscar_itens_por_pedido(conexao, pedido_id: int) -> List[ItemPedido]:
    """Recupera todos os itens vinculados a um pedido específico."""
    sql = """
        SELECT ip.id, ip.pedido_id, ip.item_cardapio_id, ip.quantidade, 
               ip.preco_unitario, ip.observacao, c.nome, c.codigo
        FROM itens_pedido ip
        JOIN cardapio c ON ip.item_cardapio_id = c.id
        WHERE ip.pedido_id = ? ORDER BY ip.id ASC;
    """
    linhas = conexao.execute(sql, (pedido_id,)).fetchall()
    return [
        ItemPedido(
            id=l["id"],
            pedido_id=l["pedido_id"],
            item_cardapio_id=l["item_cardapio_id"],
            quantidade=l["quantidade"],
            preco_unitario=float(l["preco_unitario"]),
            observacao=l["observacao"],
            nome_item=l["nome"],
            codigo_item=l["codigo"],
        )
        for l in linhas
    ]


def obter_pedido_por_id(pedido_id: int) -> Optional[Pedido]:
    """Busca um pedido completo pelo seu identificador único."""
    sql = """
        SELECT p.id, p.mesa_id, p.data_hora, p.status, p.valor_total, m.numero AS mesa_numero
        FROM pedidos p JOIN mesas m ON p.mesa_id = m.id WHERE p.id = ?;
    """
    with obter_conexao() as conexao:
        linha = conexao.execute(sql, (pedido_id,)).fetchone()
        if not linha:
            return None
        itens = buscar_itens_por_pedido(conexao, pedido_id)
        return Pedido(
            id=linha["id"],
            mesa_id=linha["mesa_id"],
            data_hora=str(linha["data_hora"]),
            status=linha["status"],
            valor_total=float(linha["valor_total"]),
            mesa_numero=linha["mesa_numero"],
            itens=itens,
        )


def obter_pedido_ativo_mesa(mesa_numero: int) -> Optional[Pedido]:
    """Localiza o pedido em aberto para uma determinada mesa."""
    sql = """
        SELECT p.id FROM pedidos p
        JOIN mesas m ON p.mesa_id = m.id
        WHERE m.numero = ? AND p.status NOT IN ('PAGO', 'CANCELADO')
        ORDER BY p.id DESC LIMIT 1;
    """
    with obter_conexao() as conexao:
        linha = conexao.execute(sql, (mesa_numero,)).fetchone()
        return obter_pedido_por_id(linha["id"]) if linha else None


def listar_pedidos(apenas_ativos: bool = False) -> List[Pedido]:
    """Lista pedidos do restaurante com opção de filtro por status ativos."""
    sql = """
        SELECT p.id, p.mesa_id, p.data_hora, p.status, p.valor_total, m.numero AS mesa_numero
        FROM pedidos p JOIN mesas m ON p.mesa_id = m.id
    """
    if apenas_ativos:
        sql += " WHERE p.status NOT IN ('PAGO', 'CANCELADO')"
    sql += " ORDER BY p.data_hora DESC;"
    with obter_conexao() as conexao:
        linhas = conexao.execute(sql).fetchall()
        pedidos = []
        for l in linhas:
            itens = buscar_itens_por_pedido(conexao, l["id"])
            pedidos.append(Pedido(
                id=l["id"], mesa_id=l["mesa_id"], data_hora=str(l["data_hora"]),
                status=l["status"], valor_total=float(l["valor_total"]),
                mesa_numero=l["mesa_numero"], itens=itens
            ))
        return pedidos


def validar_dados_abertura(mesa_numero: int, codigo: str, qtd: int) -> Tuple[bool, str, any, any]:
    """Valida a existência e capacidade de atendimento de mesa e item."""
    if qtd <= 0:
        return False, "Quantidade deve ser maior que zero.", None, None
    mesa = obter_mesa_por_numero(mesa_numero)
    if not mesa:
        return False, f"Mesa {mesa_numero} não cadastrada.", None, None
    item = obter_item_por_codigo(codigo)
    if not item or not item.disponivel:
        return False, f"Item '{codigo}' inexistente ou indisponível.", None, None
    return True, "Dados validados.", mesa, item


def criar_pedido_com_item(
    mesa_num: int, cod_item: str, qtd: int, obs: str = ""
) -> Tuple[bool, str, Optional[int]]:
    """Abre um novo pedido vinculado à mesa e insere o primeiro item."""
    valido, msg, mesa, item = validar_dados_abertura(mesa_num, cod_item, qtd)
    if not valido:
        return False, msg, None
    subtotal = item.preco * qtd
    with obter_conexao() as cx:
        cur = cx.execute(
            "INSERT INTO pedidos (mesa_id, status, valor_total) VALUES (?, 'RECEBIDO', ?);",
            (mesa.id, subtotal),
        )
        pid = cur.lastrowid
        cx.execute(
            "INSERT INTO itens_pedido (pedido_id, item_cardapio_id, quantidade, preco_unitario, observacao) VALUES (?, ?, ?, ?, ?);",
            (pid, item.id, qtd, item.preco, obs or None),
        )
        cx.commit()
    atualizar_status_mesa(mesa_num, "OCUPADA")
    return True, f"Pedido #{pid} aberto com sucesso na Mesa {mesa_num}.", pid


def adicionar_item_a_pedido(
    pedido_id: int, cod_item: str, qtd: int, obs: str = ""
) -> Tuple[bool, str]:
    """Adiciona um item ao pedido existente e recalcula o valor total."""
    if qtd <= 0:
        return False, "A quantidade deve ser positiva."
    item = obter_item_por_codigo(cod_item)
    if not item or not item.disponivel:
        return False, f"Item '{cod_item}' indisponível no cardápio."
    with obter_conexao() as cx:
        ped = cx.execute("SELECT status FROM pedidos WHERE id = ?;", (pedido_id,)).fetchone()
        if not ped or ped["status"] in ("PAGO", "CANCELADO"):
            return False, "Pedido não encontrado ou já finalizado."
        cx.execute(
            "INSERT INTO itens_pedido (pedido_id, item_cardapio_id, quantidade, preco_unitario, observacao) VALUES (?, ?, ?, ?, ?);",
            (pedido_id, item.id, qtd, item.preco, obs or None),
        )
        cx.execute(
            "UPDATE pedidos SET valor_total = valor_total + ? WHERE id = ?;",
            (item.preco * qtd, pedido_id),
        )
        cx.commit()
    return True, f"Item '{item.nome}' adicionado com sucesso."


def atualizar_status_pedido(pedido_id: int, novo_status: str) -> Tuple[bool, str]:
    """Modifica o status de produção ou entrega da comanda."""
    validos = ("RECEBIDO", "PREPARANDO", "PRONTO", "ENTREGUE", "PAGO", "CANCELADO")
    if novo_status not in validos:
        return False, f"Status '{novo_status}' inválido."
    with obter_conexao() as cx:
        cur = cx.execute("UPDATE pedidos SET status = ? WHERE id = ?;", (novo_status, pedido_id))
        cx.commit()
        if cur.rowcount == 0:
            return False, f"Pedido #{pedido_id} não localizado."
    return True, f"Status do Pedido #{pedido_id} alterado para '{novo_status}'."


def liquidar_conta_mesa(
    pedido_id: int, mesa_numero: int, aplicar_taxa: bool = True
) -> Tuple[bool, str, float]:
    """Encerra a comanda, aplica taxa de serviço opcional e libera a mesa."""
    pedido = obter_pedido_por_id(pedido_id)
    if not pedido or pedido.status in ("PAGO", "CANCELADO"):
        return False, "Pedido não está apto para fechamento.", 0.0
    taxa = (pedido.valor_total * 0.10) if aplicar_taxa else 0.0
    valor_final = round(pedido.valor_total + taxa, 2)
    with obter_conexao() as cx:
        cx.execute(
            "UPDATE pedidos SET status = 'PAGO', valor_total = ? WHERE id = ?;",
            (valor_final, pedido_id),
        )
        cx.execute("UPDATE mesas SET status = 'LIVRE' WHERE numero = ?;", (mesa_numero,))
        cx.commit()
    return True, f"Conta liquidada no valor de R$ {valor_final:.2f}.", valor_final
