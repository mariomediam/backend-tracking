from config.conexion_bd import base_de_datos
from sqlalchemy import Column, orm, types

class PruebaModel(base_de_datos.Model):
    __tablename__ = 'prueba'

    pruebaId = Column(name='id', type_=types.Integer,
                       primary_key=True, nullable=False, autoincrement=True)

    pruebaNombre = Column(
        name='nombre', type_=types.String(30), nullable=False)

    
    pruebaCorreo = Column(name='correo', type_=types.Text,
                           nullable=False, unique=True)
