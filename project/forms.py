from wtforms import Form
from wtforms import StringField, IntegerField, EmailField, validators, FileField

class ProductForm(Form):
    id = IntegerField('id', [validators.DataRequired(message='Debes llenar todos los campos')])
    name = StringField('Nombre', [validators.DataRequired(message='Debes llenar todos los campos')])
    descr = StringField('Descripcion', [validators.DataRequired(message='Debes llenar todos los campos')])
    img = FileField('File', [validators.DataRequired(message='Debes llenar todos los campos')])
    amount = IntegerField('Cantidad', [validators.DataRequired(message='Debes llenar todos los')])