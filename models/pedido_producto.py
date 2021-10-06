from sqlalchemy.sql.schema import ForeignKey
from config.conexion_bd import base_de_datos
from sqlalchemy import Column, types

class PedidoProductoModel(base_de_datos.Model):
    __tablename__ = "pedidos_productos"

    pedProdId = Column(name="ped_prod_id", type_=types.Integer, primary_key=True, autoincrement=True, nullable=False)

    pedProdCantidad = Column(name="cantidad", type_=types.Integer, nullable=False)

    pedProdPrecioUnit = Column(name="precio_unit", type_=types.DECIMAL(5, 2), nullable=False)

    pedido = Column(ForeignKey("pedidos.pedido_id"), name = "pedido_id", type_=types.Integer, nullable=False)

    producto = Column(ForeignKey("productos.prod_id"), name="prod_id", type_=types.Integer, nullable=False)

    