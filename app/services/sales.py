
from decimal import Decimal

from app import db
from app.models import Produto, Venda, ItemVenda, MovimentacaoEstoque


class RegraNegocioError(Exception):
    pass


def registrar_venda(produto_id, quantidade):
    if quantidade <= 0:
        raise RegraNegocioError(
            "Informe uma quantidade maior que zero."
        )

    produto = db.session.get(Produto, produto_id)

    if not produto or not produto.ativo:
        raise RegraNegocioError(
            "Produto não encontrado ou inativo."
        )

    if produto.quantidade_estoque < quantidade:
        raise RegraNegocioError(
            f"Estoque insuficiente. Disponível: {produto.quantidade_estoque}."
        )

    subtotal = (
        Decimal(produto.preco) * quantidade
    ).quantize(Decimal("0.01"))

    try:
        # Cria a venda
        venda = Venda(valor_total=subtotal)
        db.session.add(venda)
        db.session.flush()

        # Cria o item da venda
        item = ItemVenda(
            venda=venda,
            produto=produto,
            quantidade=quantidade,
            preco_unitario=Decimal(produto.preco),
            subtotal=subtotal
        )

        db.session.add(item)
        db.session.flush()

        # Atualiza o estoque do produto
        produto.quantidade_estoque -= quantidade

        # Registra a movimentação de saída no estoque
        movimentacao = MovimentacaoEstoque(
            id_produto=produto.id_produto,
            id_item_venda=item.id_item_venda,
            tipo="saida",
            quantidade=quantidade,
            descricao=f"Saída da venda #{venda.id_venda}"
        )

        db.session.add(movimentacao)

        # Confirma todas as operações
        db.session.commit()

        return venda

    except Exception:
        db.session.rollback()
        raise
