from app.models import Produto, Categoria
from app        import db

class ControllerProduto():
    @classmethod
    def registerNewProduct(cls, product: Produto):
        db.session.add(product)
        db.session.commit()
    
    @classmethod
    def product_order_by_name(cls):
        return Produto.query.order_by(Produto.name).all()

    @classmethod
    def product_order_by_price(cls):
        return Produto.query.order_by(Produto.price).all()
    
    @classmethod
    def product_get_by_id(cls, id):
        return Produto.query.get_or_404(id)