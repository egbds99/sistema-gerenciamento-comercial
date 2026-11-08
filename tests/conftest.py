import pytest
from app import create_app, db
from app.services.auth import criar_usuario
@pytest.fixture()
def app(tmp_path):
    app=create_app({"TESTING":True,"WTF_CSRF_ENABLED":False,"SQLALCHEMY_DATABASE_URI":f"sqlite:///{tmp_path/'test.db'}","SECRET_KEY":"test"})
    with app.app_context():
        db.drop_all(); db.create_all(); criar_usuario("teste","SenhaForte123!")
    yield app
    with app.app_context(): db.session.remove(); db.drop_all()
@pytest.fixture()
def client(app): return app.test_client()
