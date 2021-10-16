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


            print("Pasoooooooooooooooo")
            print(precioUnit)
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

