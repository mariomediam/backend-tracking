import decimal
from flask_restful import Resource, reqparse
from sqlalchemy.sql.expression import text, true
from models.producto import ProductoModel
from config.conexion_bd import base_de_datos

class ProductoController(Resource):
    serializador = reqparse.RequestParser(bundle_errors=True)

    def post(self):
        self.serializador.add_argument(
            'productoNombre',
            required=True,
            location='json',
            help='Debe ingresar nombre',
            type=str
        )
        self.serializador.add_argument(
            'productoDescripcion',
            required=True,
            location='json',
            help='Debe ingresar descripcion',
            type=str
        )
        self.serializador.add_argument(
            'productoImagen',
            required=True,
            location='json',
            help='Debe ingresar imagen',
            type=text
        )
        self.serializador.add_argument(
            'productoPrecio',
            required=True,
            location='json',
            help='Debe ingresar precio',
            type=decimal.Decimal
        )
        self.serializador.add_argument(
            'productoStock',
            required=False,
            location='json',            
            type=int
        )
        self.serializador.add_argument(
            'productoOferta',
            required=False,
            location='json',            
            type=bool
        )
        data = self.serializador.parse_args()
        try:
            nuevo_producto : ProductoModel = ProductoModel()
            nuevo_producto.productoNombre = data.get('productoNombre')
            nuevo_producto.productoDescripcion = data.get('productoDescripcion')
            nuevo_producto.productoPrecio = data.get('productoPrecio')
            nuevo_producto.productoStock = data.get('productoStock')
            nuevo_producto.productoOferta = data.get('productoOferta')
            base_de_datos.session.add(nuevo_producto)
            base_de_datos.session.commit()
            return {
                "message": "Producto agregado exitosamente",
                "content": {
                    "productoId": nuevo_producto.productoId,
                    "productoNombre": nuevo_producto.productoNombre                    
                }

            }, 201
        except Exception as e:
            return {
                "message": "Hubo un error al guardar el producto, intentelo nuevamente",
                "content": e.args[0]
            }, 500

        