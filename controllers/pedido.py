from flask_restful import Resource, reqparse
from sqlalchemy.sql.expression import text, true
from sqlalchemy.sql.sqltypes import Integer
from models.pedido import PedidoModel
from models.cliente import ClienteModel
from config.conexion_bd import base_de_datos
from flask_jwt import jwt_required
import uuid

class PedidoController(Resource):
    serializador = reqparse.RequestParser(bundle_errors=True)

    @jwt_required()
    def post(self):

        self.serializador.add_argument(
            'pedidoDireccion',
            required=True,
            location='json',
            help='Debe ingresar dirección de entrega',
            type=str
        )
        self.serializador.add_argument(
            'pedidoDistrDestino',
            required=True,
            location='json',
            help='Debe ingresar distrito de entrega',
            type=int
        )
        self.serializador.add_argument(
            'clienteNombre',
            required=True,
            location='json',
            help='Debe ingresar nombre de cliente',
            type=str
        )
        self.serializador.add_argument(
            'clienteCorreo',
            required=True,
            location='json',
            help='Debe ingresar correo de cliente',
            type=str
        )
        self.serializador.add_argument(
            'clienteTelefono',
            required=False,
            location='json',
            type=str
        )
        data = self.serializador.parse_args()
        try:    
            

            nuevo_cliente = ClienteModel().save(
                data.get('clienteNombre'), 
                data.get('clienteCorreo'), 
                data.get('clienteTelefono'), 
                data.get('pedidoDireccion'), 
                data.get('pedidoDistrDestino')
            )

            nuevo_pedido : PedidoModel = PedidoModel()
            nuevo_pedido.pedidoToken = str(uuid.uuid4())[0:6] #"6ac21f" 
            nuevo_pedido.pedidoDireccion = data.get('pedidoDireccion')
            nuevo_pedido.pedidoDistrDestino = data.get('pedidoDistrDestino')
            nuevo_pedido.cliente = nuevo_cliente.clienteId
        
            base_de_datos.session.add(nuevo_pedido)
            base_de_datos.session.commit()
            return {
                "message": "Pedido agregado exitosamente",
                "content": {
                    "pedidoId": nuevo_pedido.pedidoId,
                    "pedidoToken": nuevo_pedido.pedidoToken                    
                }

            }, 201
        except Exception as e:
            base_de_datos.session.rollback()
            return {
                "message": "Hubo un error al guardar el pedido, intentelo nuevamente",
                "content": e.args[0]
            }, 500

