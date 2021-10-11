from flask import Flask
from flask_restful import Api
from config.conexion_bd import base_de_datos
from os import environ
from dotenv import load_dotenv
from controllers.producto import ProductoController
from models.producto import ProductoModel
from models.distrito import DistritoModel
from models.cliente import ClienteModel
from models.pedido import PedidoModel
from models.pedido_producto import PedidoProductoModel
from models.plantilla_rutas import PlantillaRutasModel
from models.pedido_ruta import PedidoRutaModel
from models.califica import CalificaModel
from models.usuario import UsuarioModel
from controllers.producto import ProductoController
from controllers.usuarios import RegistroController, LoginController, UsuarioController
from flask_jwt import JWT
from config.seguridad import autenticador, identificador
from datetime import timedelta


load_dotenv()

app = Flask(__name__)
api = Api(app)
# config => las variables de configuracion de mi proyecto de flask DEBUG=TRUE, PORT= 5000, ENVIRONMENT=DEVELOPMENT
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = environ.get('JWT_SECRET')
app.config['JWT_EXPIRATION_DELTA'] = timedelta(days=1)

jsonwebtoken = JWT(app=app, authentication_handler=autenticador,
                   identity_handler=identificador)


base_de_datos.init_app(app)
#base_de_datos.drop_all(app=app)
base_de_datos.create_all(app=app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

# ZONA DE ENRUTAMIENTO
api.add_resource(ProductoController, '/productos')
api.add_resource(RegistroController, '/registro')
api.add_resource(LoginController, "/login")
api.add_resource(UsuarioController, "/usuario")

if __name__ == '__main__':
    app.run(debug=True)    