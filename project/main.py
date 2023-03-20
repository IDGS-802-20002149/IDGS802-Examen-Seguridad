from flask import Blueprint, render_template
from flask_security import login_required, current_user
from flask_security.decorators import roles_accepted, roles_required
from . import db
from .models import User

main = Blueprint('main', __name__)

#Definimos la ruta para la página principal
@main.route('/')
def index():
    return render_template('index.html')

#Definimos la ruta para la página de perfil de usuario
@main.route('/profile')
@login_required
@roles_accepted('user', 'admin')
def profile():
    return render_template('profile.html', name = current_user.name)


@main.route('/profile2')
@login_required
@roles_accepted('user', 'admin')
def profile2():
    return render_template('profile2.html', name = current_user.name)