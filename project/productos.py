from flask import Blueprint, render_template, url_for, request, redirect
from flask_security import login_required 
from flask_security.decorators import roles_accepted, roles_required
from .models import Product
from . import db
from . import forms
from .dbp import get_connection
import base64
import io
from PIL import Image
import zlib

productos = Blueprint('productos', __name__)

@productos.route('/getProducts', methods=['GET'])
@login_required
@roles_accepted('admin')
def getProducts():
    form = forms.ProductForm(request.form)
    product = Product.query.all()
    
    return render_template('getProducts.html', form = form, product = product)

@productos.route('/getProductsCustom', methods=['GET'])
@login_required
@roles_accepted('user', 'admin')
def getProductsCustom():
    form = forms.ProductForm(request.form)
    product = Product.query.all()
    
    return render_template('getProductsCustom.html', form = form, product = product)

@productos.route('/insertProduct', methods=['GET','POST'])
@login_required
@roles_accepted('admin')
def insertProduct():
    form = forms.ProductForm(request.form)
    if request.method == 'POST':

        name = form.name.data,
        descr = form.descr.data,
        amount = form.amount.data
        try:
            connection  = get_connection()
            with connection.cursor() as cursor:
                cursor.execute('call insertProduct(%s,%s,%s,%s)',(name,descr,upload_image(), amount))
            connection.commit()
            connection.close()
        except Exception as ex:
            print(ex)
        return redirect(url_for('productos.getProducts'))

    return render_template('insertProduct.html', form=form)

@productos.route('/updateProduct', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def updateProduct():
    form = forms.ProductForm(request.form)
    if request.method == 'GET':
        id = request.args.get('id')
        product1 = db.session.query(Product).filter(Product.id==id).first()
        form.id.data = request.args.get('id')
        form.name.data = product1.name
        form.descr.data = product1.descr
        form.img.data = product1.img
        form.amount.data = product1.amount
    
    if request.method == 'POST':
        id = form.id.data
        product = db.session.query(Product).filter(Product.id==id).first()
        product.name = form.name.data
        product.descr = form.descr.data
        product.img = form.img.data
        product.amount = form.amount.data

        db.session.add(product)
        db.session.commit()
        return redirect(url_for('productos.getProducts'))
    return render_template('updateProduct.html', form=form)

@productos.route('/deleteProduct', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def deleteProduct():
    form = forms.ProductForm(request.form)
    if request.method == 'GET':
        id = request.args.get('id')
        product1 = db.session.query(Product).filter(Product.id==id).first()
        form.id.data = request.args.get('id')
        form.name.data = product1.name
        form.descr.data = product1.descr
        form.img.data = product1.img
        form.amount.data = product1.amount
    
    if request.method == 'POST':
        id = form.id.data
        print(id)
        product = db.session.query(Product).filter(Product.id==id).first()
        product.name = form.name.data
        product.descr = form.descr.data
        product.img = form.img.data
        product.amount = form.amount.data

        db.session.delete(product)
        db.session.commit()
        return redirect(url_for('productos.getProducts'))
    return render_template('deleteProduct.html', form=form)

def upload_image():
   
    image_file = request.files["img"]
    
    # Convertir la imagen a un objeto Pillow
    img = Image.open(image_file)

    # Codificar la imagen en base64
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    encoded_string = base64.b64encode(buffered.getvalue()).decode('utf-8')

    # Enviar la respuesta de vuelta a HTML
    return encoded_string
