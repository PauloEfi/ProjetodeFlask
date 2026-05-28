from app        import app
from flask      import Flask, render_template, redirect, url_for, request, flash
from datetime   import datetime
from typing     import Final
from app.models import db, Produto, Categoria
from app.forms  import ProdutoForm

from app.controllers.controllerProduto import ControllerProduto

PAGE_PRODUCT_LIST:     Final[str] = "productList.html"
PAGE_PRODUCT_REGISTER: Final[str] = "productRegister.html"
PAGE_PRODUCT_INFO:     Final[str] = "productDetails.html"
HOME_PAGE:             Final[str] = "index.html"  

@app.route('/')
def index():
    return render_template(HOME_PAGE)

# 1. Rota de Cadastro
@app.route('/produto/novo', methods = ['GET', 'POST'])
def cadastrar_produto():
    form = ProdutoForm()
    # Carrega as categorias dinamicamente no SelectField
    form.categoria_id.choices = [(c.id, c.name) for c in Categoria.query.order_by('name').all()]
    # PARA DEBUG
    # if request.method == 'POST':
    #     form.validate()
    #     print("MÉTODO:", request.method)
    #     print("DADOS DO FORMULÁRIO:", request.form)
    #     print("ERROS DETECTADOS:", form.errors)
    if form.validate_on_submit():
        form.saveData()
        flash('Produto cadastrado com sucesso!', 'success')
        return redirect(url_for('listar_produtos'))
    return render_template(PAGE_PRODUCT_REGISTER, form = form)

# 2. Rota de Listagem Ordenada
@app.route('/produtos')
def listar_produtos():
    orderProduct_by = request.args.get('ordem', 'nome') # Valor default: 'nome'
    if orderProduct_by == 'preco':
        produtos = ControllerProduto.product_order_by_price()
    else:
        produtos = ControllerProduto.product_order_by_name()
        
    return render_template(PAGE_PRODUCT_LIST, produtos = produtos, ordem_atual = orderProduct_by)

# 3. Visualização (Rota Dinâmica)
@app.route('/produto/<int:id>')
def visualizar_produto(id):
    product = ControllerProduto.product_get_by_id(id)
    return render_template(PAGE_PRODUCT_INFO, produto = product)


@app.route('/produto/editar/<int:id>', methods=['GET', 'POST'])
def editar_produto(id):
    product = ControllerProduto.product_get_by_id(id)
    form = ProdutoForm()
    form.categoria_id.choices = [(c.id, c.name) for c in Categoria.query.order_by('name').all()]
    # Pre-popula os dados no formulário (GET)
    if request.method == 'GET':
        form.name.data = product.name
        form.price.data = product.price
        form.quantity.data = product.quantity
        form.manufacturing_date.data = product.manufacturing_date
        form.expiration_date.data = product.expiration_date
        form.manufacturer.data = product.manufacturer
        form.categoria_id.data = product.categoria_id

    if form.validate_on_submit():
        product.name = form.name.data
        product.price = form.price.data
        product.quantity = form.quantity.data
        product.manufacturing_date = form.manufacturing_date.data
        product.expiration_date = form.expiration_date.data
        product.manufacturer = form.manufacturer.data
        product.categoria_id = form.categoria_id.data
        ControllerProduto.update_product(product)
        flash('Produto atualizado com sucesso!', 'success')
        return redirect(url_for('listar_produtos'))

    return render_template(PAGE_PRODUCT_REGISTER, form = form, edit = True)


# Rota de Exclusão
@app.route('/produto/excluir/<int:id>', methods=['POST'])
def excluir_produto(id):
    product = ControllerProduto.product_get_by_id(id)
    ControllerProduto.delete_product(product)
    flash('Produto excluído com sucesso!', 'success')
    return redirect(url_for('listar_produtos'))


# Rota de Relatórios - quantidade de produtos por categoria
@app.route('/relatorios')
def relatorios():
    counts = db.session.query(Categoria.name, func.count(Produto.id)).outerjoin(Produto).group_by(Categoria.id).all()
    # counts: list of tuples (category_name, count)
    return render_template('reports.html', counts = counts)