from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models import Produto, Venda
from app.services.sales import registrar_venda, RegraNegocioError
bp=Blueprint("sales",__name__)
@bp.get("/nova")
@login_required
def nova(): return render_template("sale_form.html", produtos=Produto.query.filter_by(ativo=True).order_by(Produto.nome).all())
@bp.post("/registrar")
@login_required
def registrar():
    try:
        venda=registrar_venda(int(request.form.get("produto_id","")),int(request.form.get("quantidade","")))
        flash("Venda registrada com sucesso.","success")
        return redirect(url_for("sales.resultado",vid=venda.id_venda))
    except (ValueError,TypeError): flash("Selecione um produto e informe uma quantidade válida.","error")
    except RegraNegocioError as e: flash(str(e),"error")
    return redirect(url_for("sales.nova"))
@bp.get("/resultado/<int:vid>")
@login_required
def resultado(vid):
    venda=Venda.query.get_or_404(vid)
    alertas=Produto.query.filter_by(ativo=True).filter(Produto.quantidade_estoque<=Produto.estoque_minimo).all()
    return render_template("sale_result.html",venda=venda,alertas=alertas)
@bp.get("/historico")
@login_required
def historico(): return render_template("history.html",vendas=Venda.query.order_by(Venda.data_venda.desc()).all())
