from flask import Flask
from flask_restful import Api
from config.conexion_bd import base_de_datos
from os import environ
from dotenv import load_dotenv
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
from controllers.producto import ProductoController
from controllers.usuarios import RegistroController, LoginController, UsuarioController
from controllers.distrito import DistritosController, DistritoController, DistritosControllerFiltrar
from controllers.pedido import PedidosController, PedidoController, PedidoControllerFiltrar
from controllers.cliente import ClientesController, ClienteController, ClientesControllerFiltrar
from controllers.pedido_producto import PedidoProductosController
from controllers.pedido_ruta import PedidoRutaControllerPorPedidoId
from controllers.reportes import ReporteControllerVentasPorDistrito, ReporteControllerVentasPorProducto, ReporteControllerVentasPorCliente
from flask_jwt import JWT
from config.seguridad import autenticador, identificador
from datetime import timedelta
from flask_cors import CORS



load_dotenv()

app = Flask(__name__)
CORS(app=app, origins='*', methods=['GET',
     'POST', 'PUT', 'DELETE'], allow_headers='Content-Type')

api = Api(app)
# config => las variables de configuracion de mi proyecto de flask DEBUG=TRUE, PORT= 5000, ENVIRONMENT=DEVELOPMENT
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = environ.get('JWT_SECRET')
app.config['JWT_EXPIRATION_DELTA'] = timedelta(days=1)
app.config["PATH_STATIC"] ="./static"

jsonwebtoken = JWT(app=app, authentication_handler=autenticador,
                   identity_handler=identificador)


base_de_datos.init_app(app)
# base_de_datos.drop_all(app=app)
base_de_datos.create_all(app=app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

# ZONA DE ENRUTAMIENTO
api.add_resource(ProductoController, '/productos')
api.add_resource(RegistroController, '/registro')
api.add_resource(LoginController, "/login")
api.add_resource(UsuarioController, "/usuario")
api.add_resource(DistritosController, "/distritos")
api.add_resource(DistritoController, "/distrito/<int:id>")
api.add_resource(DistritosControllerFiltrar, "/buscar_distrito")
api.add_resource(PedidosController, "/pedidos")
api.add_resource(PedidoController, "/pedido/<int:id>")
api.add_resource(ClientesController, "/clientes")
api.add_resource(ClienteController, "/cliente/<int:id>")
api.add_resource(ClientesControllerFiltrar, "/buscar_cliente")
api.add_resource(PedidoProductosController, "/pedido_productos")
api.add_resource(PedidoControllerFiltrar, "/buscar_pedido")
api.add_resource(PedidoRutaControllerPorPedidoId, "/buscar_pedido_ruta")
api.add_resource(ReporteControllerVentasPorDistrito, "/reporte_venta_distrito")
api.add_resource(ReporteControllerVentasPorProducto, "/reporte_venta_producto")
api.add_resource(ReporteControllerVentasPorCliente, "/reporte_venta_cliente")
if __name__ == '__main__':
    app.run(debug=True)    