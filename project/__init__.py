import os
from flask import Flask
from flask_security import Security, SQLAlchemyUserDatastore
from flask_sqlalchemy import SQLAlchemy

#Creamos una instancia de SQLAlchemy
db = SQLAlchemy()
from .models import User, Role

#Creamos un objeto de SQLAlchemyUserDataStore
userDataStore = SQLAlchemyUserDatastore(db, User, Role)


#Metodo de inicio de SQLAlchemy
def create_app():
    # Creamos nuestra aplicacion de Flask
    app = Flask(__name__)

    #Configuraciones necesarias
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.urandom(24)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/amazon'
    app.config['SECURITY_PASSWORD_HASH'] = 'pbkdf2_sha256'
    app.config['SECURITY_PASSWORD_SALT'] = 'secretsalt'

    db.init_app(app)
    #Metodo para crear la BD en la primera ejecucion
    @app.before_first_request
    def create_all():
        db.create_all()

    #Conectando los modelos de FLASK-SECURITY usando SQLAlchemyUserDataStore
    security = Security(app, userDataStore)

    #Registramos dos blueprints
    from .auth import auth as main_blueprint
    app.register_blueprint(main_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .productos import productos as main_blueprint
    app.register_blueprint(main_blueprint)

    return app