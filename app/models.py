from datetime import datetime
from flask_login import UserMixin
from app import db, login_manager

class Usuario(UserMixin, db.Model):
    __tablename__ = "usuarios"
    id_usuario = db.Column(db.Integer, primary_key=True)
    nome_acesso = db.Column(db.String(80), unique=True, nullable=False)
    hash_senha = db.Column(db.String(255), nullable=False)
    ativo = db.Column(db.Boolean, default=True, nullable=False)
    def get_id(self): return str(self.id_usuario)

@login_manager.user_loader
def load_user(user_id): return db.session.get(Usuario, int(user_id))

class Produto(db.Model):
    __tablename__ = "produtos"
    id_produto = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    categoria = db.Column(db.String(60))
    preco = db.Column(db.Numeric(10,2), nullable=False)
    quantidade_estoque = db.Column(db.Integer, nullable=False, default=0)
    estoque_minimo = db.Column(db.Integer, nullable=False, default=0)
    ativo = db.Column(db.Boolean, nullable=False, default=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    itens = db.relationship("ItemVenda", back_populates="produto")
    @property
    def estoque_baixo(self): return self.quantidade_estoque <= self.estoque_minimo

class Venda(db.Model):
    __tablename__ = "vendas"
    id_venda = db.Column(db.Integer, primary_key=True)
    data_venda = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    valor_total = db.Column(db.Numeric(10,2), nullable=False)
    status = db.Column(db.String(20), default="concluida", nullable=False)
    itens = db.relationship("ItemVenda", back_populates="venda", cascade="all, delete-orphan")

class ItemVenda(db.Model):
    __tablename__ = "itens_venda"
    id_item_venda = db.Column(db.Integer, primary_key=True)
    id_venda = db.Column(db.Integer, db.ForeignKey("vendas.id_venda"), nullable=False)
    id_produto = db.Column(db.Integer, db.ForeignKey("produtos.id_produto"), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Numeric(10,2), nullable=False)
    subtotal = db.Column(db.Numeric(10,2), nullable=False)
    venda = db.relationship("Venda", back_populates="itens")
    produto = db.relationship("Produto", back_populates="itens")

class MovimentacaoEstoque(db.Model):
    __tablename__ = "movimentacoes_estoque"
    id_movimentacao = db.Column(db.Integer, primary_key=True)
    id_produto = db.Column(db.Integer, db.ForeignKey("produtos.id_produto"), nullable=False)
    id_item_venda = db.Column(db.Integer, db.ForeignKey("itens_venda.id_item_venda"))
    tipo = db.Column(db.String(20), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    data_movimentacao = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    descricao = db.Column(db.String(200))
