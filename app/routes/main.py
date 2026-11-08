from flask import Blueprint, render_template
from flask_login import login_required
from app.models import Produto, Venda
bp = Blueprint("main", __name__)
@bp.get("/")
@login_required
def dashboard():
    alertas = Produto.query.filter_by(ativo=True).filter(Produto.quantidade_estoque <= Produto.estoque_minimo).all()
    return render_template("dashboard.html", produtos_ativos=Produto.query.filter_by(ativo=True).count(),
                           alertas=alertas, vendas=Venda.query.order_by(Venda.data_venda.desc()).limit(5).all())
