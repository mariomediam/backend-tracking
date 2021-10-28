from sqlalchemy.sql.sqltypes import DECIMAL
from config.conexion_bd import base_de_datos
from flask_restful import Resource, reqparse
from models.pedido import PedidoModel
from models.pedido_producto import PedidoProductoModel
from models.producto import ProductoModel

class PedidoProductosController(Resource):
    serializador = reqparse.RequestParser(bundle_errors=True)

    def post(self):
        self.serializador.add_argument(
            'pedProdCantidad',
            required=True,
            location='json',
            help='Debe ingresar cantidad',
            type=int
        )
        self.serializador.add_argument(
            'pedProdPrecioUnit',            
            location='json',
            type=float
        )
        self.serializador.add_argument(
            'pedido',
            required=True,
            location='json',
            help='Debe ingresar código de pedido',
            type=int
        )
        self.serializador.add_argument(
            'producto',
            required=True,
            location='json',
            help='Debe ingresar codigo de producto',
            type=int
        )

        data = self.serializador.parse_args()
        try:
            pedido_buscado = base_de_datos.session.query(PedidoModel).filter(PedidoModel.pedidoId==data.get('pedido')).first()

            if not pedido_buscado:
                raise Exception("El pedido no existe")
            
            producto_buscado = base_de_datos.session.query(ProductoModel).filter(ProductoModel.productoId==data.get('producto')).first()

            if not producto_buscado:
                raise Exception("El producto no existe")

            if not data.get('pedProdPrecioUnit'):
                precioUnit = producto_buscado.productoPrecio
            else:
                precioUnit = data.get('pedProdPrecioUnit')

            nuevo_pedido_producto : PedidoProductoModel = PedidoProductoModel()            
            nuevo_pedido_producto.pedProdCantidad = data.get('pedProdCantidad')
            nuevo_pedido_producto.pedProdPrecioUnit = precioUnit
            nuevo_pedido_producto.pedido = data.get('pedido')
            nuevo_pedido_producto.producto = data.get('producto')
            
            
            base_de_datos.session.add(nuevo_pedido_producto)
            base_de_datos.session.commit()
            return {
                "message": "Producto agregado exitosamente",
                "content": {
                    "pedidoProductoId": nuevo_pedido_producto.pedProdId,
                    "productoNombre": producto_buscado.productoNombre,
                    "cantidad": nuevo_pedido_producto.pedProdCantidad,
                    "precioUnitario": float(nuevo_pedido_producto.pedProdPrecioUnit),
                    "subTotal": float(nuevo_pedido_producto.pedProdCantidad * nuevo_pedido_producto.pedProdPrecioUnit)
                }

            }, 201
        except Exception as e:
            return {
                "message": "Hubo un error al guardar el producto, intentelo nuevamente",
                "content": e.args[0]
            }, 500


class PedidoProductoControllerPorPedidoId(Resource):

    def __init__(self):
        self.serializadorFiltro = reqparse.RequestParser()
        self.serializadorFiltro.add_argument(
            'pedidoId',
            location='args',
            required=True,
            type=str
        )

    def get(self):
        filtros = self.serializadorFiltro.parse_args()
        resultado = base_de_datos.session.query(PedidoProductoModel).filter(PedidoProductoModel.pedido==filtros["pedidoId"]).all()
        
        resultado_final = []
        if resultado:
            
            for registro in resultado:
                resultado = registro.__dict__
                del resultado['_sa_instance_state']                

                producto_buscado = base_de_datos.session.query(ProductoModel).filter(ProductoModel.productoId==resultado['producto']).first()
                
                resultado['pedProdPrecioUnit'] = float(resultado['pedProdPrecioUnit'])                
                resultado['productoDescripcion'] = producto_buscado.__dict__['productoDescripcion']
                resultado['productoImagen'] = producto_buscado.__dict__['productoImagen']
                resultado['productoNombre'] = producto_buscado.__dict__['productoNombre']

                resultado_final.append(resultado)                            
            return {
                "message": "Registros encontrados",
                "content": resultado_final
            }
        else:
            return {
                "message": "No se encontraron registros coincidentes",
                "content": resultado_final
            }, 200