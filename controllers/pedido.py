from flask_restful import Resource, reqparse
from sqlalchemy.sql.expression import text, true
from sqlalchemy.sql.sqltypes import ARRAY, Integer
from models.pedido import PedidoModel
from models.cliente import ClienteModel
from config.conexion_bd import base_de_datos
from flask_jwt import jwt_required
import uuid

from models.pedido_producto import PedidoProductoModel

class PedidosController(Resource):
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
        self.serializador.add_argument(
            'pedProductos',
            required=True,
            location='json',
            type=list
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
            nuevo_pedido.pedidoToken = str(uuid.uuid4())[0:6]  #"6ac21f"
            nuevo_pedido.pedidoDireccion = data.get('pedidoDireccion')
            nuevo_pedido.pedidoDistrDestino = data.get('pedidoDistrDestino')
            nuevo_pedido.cliente = nuevo_cliente.clienteId
        
            base_de_datos.session.add(nuevo_pedido)

            base_de_datos.session.commit()

            pedProductos = data.get('pedProductos')
            for producto in pedProductos:
                nuevo_pedProducto = PedidoProductoModel.agregar(nuevo_pedido.pedidoId, producto.get("producto"), producto.get("pedProdCantidad"))

                base_de_datos.session.add(nuevo_pedProducto)

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

    @jwt_required()
    def get(self):
        pedidos = base_de_datos.session.query(PedidoModel).all()
        resultado = []
        for pedido in pedidos:
            pedido_dicc = pedido.__dict__            
            del pedido_dicc['_sa_instance_state']
            pedido_dicc['pedidoFecha'] = str(pedido_dicc['pedidoFecha'])
            resultado.append(pedido_dicc)

        return {
            "message": None,
            "content": resultado
        }

class PedidoController(Resource):
    def get(self, id):
        resultado = base_de_datos.session.query(
            PedidoModel).filter(PedidoModel.pedidoId == id).first()

        if resultado:
            data = resultado.__dict__
            del data['_sa_instance_state']
            data['pedidoFecha'] = str(data['pedidoFecha'])
            return {
                "message": "pedido",
                "content": data
            }
        else:
            return {
                "message": "El pedido no existe",
                "content": resultado
            }, 404        