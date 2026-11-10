from decimal import Decimal
import pytest
from app import db
from app.models import Produto
from app.services.sales import registrar_venda, RegraNegocioError
def test_venda_atualiza_estoque(app):
    with app.app_context():
        p=Produto(nome="Café 500 g",preco=Decimal("18.00"),quantidade_estoque=12,estoque_minimo=5)
        db.session.add(p); db.session.commit()
        venda=registrar_venda(p.id_produto,2)
        assert venda.valor_total==Decimal("36.00")
        assert db.session.get(Produto,p.id_produto).quantidade_estoque==10
def test_bloqueia_estoque_insuficiente(app):
    with app.app_context():
        p=Produto(nome="Arroz",preco=Decimal("7.50"),quantidade_estoque=1,estoque_minimo=2)
        db.session.add(p); db.session.commit()
        with pytest.raises(RegraNegocioError): registrar_venda(p.id_produto,2)
        assert db.session.get(Produto,p.id_produto).quantidade_estoque==1
def test_rota_requer_login(client):
    assert client.get("/").status_code==302
