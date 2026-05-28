from app      import db
from datetime import datetime

class Categoria(db.Model):
    id   = db.Column(db.Integer,    primary_key = True,  autoincrement = True)
    name = db.Column(db.String(50), nullable    = True, unique         = True)
    # Relacionamento que permite acessar produtos de uma categoria: categoria.produtos
    products = db.relationship('Produto', backref = 'categoria', lazy = True)

class Produto(db.Model):
    id                 = db.Column(db.Integer,     primary_key = True)
    registerDate       = db.Column(db.DateTime,    nullable    = True, default = datetime.utcnow())
    name               = db.Column(db.String(100), nullable    = True)
    price              = db.Column(db.Float,       nullable    = True)
    quantity           = db.Column(db.Integer,     nullable    = True)
    manufacturing_date = db.Column(db.Date,        nullable    = True)
    expiration_date    = db.Column(db.Date,        nullable    = True)
    manufacturer       = db.Column(db.String(100), nullable    = True)
    # Chave Estrangeira
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable = True)