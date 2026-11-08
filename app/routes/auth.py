from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from app.models import Usuario
from app.services.auth import verificar_senha
bp = Blueprint("auth", __name__)
@bp.route("/login", methods=["GET","POST"])
def login():
    if current_user.is_authenticated: return redirect(url_for("main.dashboard"))
    if request.method == "POST":
        user = Usuario.query.filter_by(nome_acesso=request.form.get("nome_acesso","").strip(), ativo=True).first()
        if user and verificar_senha(user, request.form.get("senha","")):
            login_user(user); return redirect(url_for("main.dashboard"))
        flash("Usuário ou senha inválidos. Confira os dados.", "error")
    return render_template("login.html")
@bp.post("/sair")
def logout():
    logout_user(); return redirect(url_for("auth.login"))
