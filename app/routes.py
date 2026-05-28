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

# @app.route('/produto/editar/<int:id>', methods=['GET', 'POST'])
# @app.route('/produto/excluir/<int:id>', methods=['POST'])
# @app.route('/categorias/relatorio')