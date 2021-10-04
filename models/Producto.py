from config.conexion_bd import base_de_datos
from sqlalchemy import Column, orm, types

class ProductoModel(base_de_datos.Model):
    __tablename__ = 'productos'

    productoId = Column(name='prod_id', type_=types.Integer,
                       primary_key=True, nullable=False, autoincrement=True)

    productoNombre = Column(
        name='nombre', type_=types.String(50), nullable=False)

    productoDescripcion = Column(
        name='descripcion', type_=types.String(100), nullable=False)

    productoImagen = Column(name='imagen', type_=types.Text, nullable=True)

    productoPrecio = Column(name='precio', type_=types.DECIMAL(5,2),  nullable=True)

    productoStock = Column(name='stock', type_=types.Integer, 
                           nullable=False, unique=True, mini)

    usuarioOferta = Column(name='oferta', type_=types.Boolean, nullable=False, default=False)

