from decimal import Decimal, InvalidOperation
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models import Produto, MovimentacaoEstoque
bp = Blueprint("products", __name__)
@bp.get("/")
@login_required
def index():
    q=request.args.get("q","").strip()
    query=Produto.query
    if q: query=query.filter(Produto.nome.ilike(f"%{q}%"))
    return render_template("products.html", produtos=query.order_by(Produto.nome).all(), termo=q)
@bp.route("/novo", methods=["GET","POST"])
@login_required
def novo():
    if request.method=="POST":
        try:
            nome=request.form.get("nome","").strip()
            preco=Decimal(request.form.get("preco","").replace(",","."))
            qtd=int(request.form.get("quantidade_estoque",""))
            minimo=int(request.form.get("estoque_minimo",""))
            if not nome or preco<0 or qtd<0 or minimo<0: raise ValueError
        except (ValueError,InvalidOperation):
            flash("Confira os campos obrigatórios e use valores não negativos.","error")
            return render_template("product_form.html")
        p=Produto(nome=nome,categoria=request.form.get("categoria","").strip() or None,
                  preco=preco,quantidade_estoque=qtd,estoque_minimo=minimo)
        db.session.add(p); db.session.flush()
        if qtd: db.session.add(MovimentacaoEstoque(produto=p,tipo="entrada",quantidade=qtd,descricao="Estoque inicial"))
        db.session.commit(); flash("Produto cadastrado com sucesso.","success")
        return redirect(url_for("products.index"))
    return render_template("product_form.html")
@bp.post("/<int:pid>/inativar")
@login_required
def inativar(pid):
    p=db.get_or_404(Produto,pid); p.ativo=False; db.session.commit()
    flash("Produto inativado; histórico preservado.","success")
    return redirect(url_for("products.index"))
