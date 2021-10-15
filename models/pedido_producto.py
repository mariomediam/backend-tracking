from sqlalchemy.sql.schema import ForeignKey
from config.conexion_bd import base_de_datos
from sqlalchemy import Column, types

from models.producto import ProductoModel

class PedidoProductoModel(base_de_datos.Model):
    __tablename__ = "pedidos_productos"

    pedProdId = Column(name="ped_prod_id", type_=types.Integer, primary_key=True, autoincrement=True, nullable=False)

    pedProdCantidad = Column(name="cantidad", type_=types.Integer, nullable=False)

    pedProdPrecioUnit = Column(name="precio_unit", type_=types.DECIMAL(5, 2), nullable=False)

    pedido = Column(ForeignKey("pedidos.pedido_id"), name = "pedido_id", type_=types.Integer, nullable=False)

    producto = Column(ForeignKey("productos.prod_id"), name="prod_id", type_=types.Integer, nullable=False)

    def agregar(pedido_id, prod_id, cantidad):

        producto_buscado : ProductoModel = base_de_datos.session.query(ProductoModel).filter(ProductoModel.productoId==prod_id).first()

        if not producto_buscado:            
            raise Exception("El producto prod_id: {} no existe ".format(prod_id))

        pedido_producto = PedidoProductoModel()
        pedido_producto.pedProdCantidad = cantidad
        pedido_producto.pedProdPrecioUnit = producto_buscado.productoPrecio
        pedido_producto.pedido = pedido_id
        pedido_producto.producto = prod_id

        return pedido_producto

    