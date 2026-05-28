from flask_wtf          import FlaskForm
from wtforms            import StringField, FloatField, IntegerField, DateField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional
from app.models         import Produto
from app.controllers.controllerProduto import ControllerProduto

class ProdutoForm(FlaskForm):
    name               = StringField('Nome do Produto',           validators=[DataRequired()])
    price              = FloatField('Preço',                      validators=[DataRequired(), NumberRange(min = 0.01)])
    quantity           = IntegerField('Quantidade Disponível',    validators=[DataRequired(), NumberRange(min = 0)])
    manufacturing_date = DateField('Data de Fabricação',          validators=[DataRequired()], format='%Y-%m-%d')
    expiration_date    = DateField('Data de Validade (Opcional)', format='%Y-%m-%d', validators=[Optional()])
    manufacturer       = StringField('Fabricante',                validators=[DataRequired()])
    # Parâmetro "Coercion" para int garante que o ID da categoria retorne como número
    categoria_id       = SelectField('Categoria', coerce = int, validators=[DataRequired()])
    submit             = SubmitField('Salvar Produto')

    def saveData(self):
        new_product = Produto(
            name               = self.name.data,
            price              = self.price.data,
            quantity           = self.quantity.data,
            manufacturing_date = self.manufacturing_date.data,
            expiration_date    = self.expiration_date.data,
            manufacturer       = self.manufacturer.data,
            categoria_id       = self.categoria_id.data)
        # Salva novo produto no banco de dados
        ControllerProduto.registerNewProduct(new_product)
        