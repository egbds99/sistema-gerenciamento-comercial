from pathlib import Path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    if test_config: app.config.update(test_config)
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    db.init_app(app); login_manager.init_app(app); csrf.init_app(app)
    login_manager.login_view = "auth.login"
    from app.models import Usuario
    from app.routes import auth, main, products, sales
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(products.bp, url_prefix="/produtos")
    app.register_blueprint(sales.bp, url_prefix="/vendas")
    @app.cli.command("init-db")
    def init_db():
        db.create_all()
        print("Banco inicializado.")
    @app.cli.command("create-admin")
    def create_admin():
        import os
        from app.services.auth import criar_usuario
        user, password = os.getenv("ADMIN_USERNAME"), os.getenv("ADMIN_PASSWORD")
        if not user or not password: raise SystemExit("Defina ADMIN_USERNAME e ADMIN_PASSWORD.")
        if Usuario.query.filter_by(nome_acesso=user).first(): print("Usuário já existe.")
        else: criar_usuario(user, password); print("Administrador criado.")
    with app.app_context(): db.create_all()
    return app
