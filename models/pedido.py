from sqlalchemy.sql.expression import null
from sqlalchemy.sql.schema import ForeignKey
from config.conexion_bd import base_de_datos
from sqlalchemy import Column, orm, types
from sqlalchemy.sql.sqltypes import ARRAY, String
from datetime import datetime

class PedidoModel(base_de_datos.Model):
    __tablename__ = "pedidos"

    pedidoId = Column(name="pedido_id", type_=types.Integer, primary_key=True, nullable=False, autoincrement=True)

    pedidoToken = Column(name="token", type_=types.String(20), unique=True, nullable=False)

    pedidoFecha = Column(name="fecha", type_=types.DateTime(), default=datetime.utcnow)

    pedidoDireccion = Column(name="direccion", type_=types.String(50), nullable=False)

    pedidoGeo = Column(name="pedido_dirgeo", type_=types.ARRAY(String), nullable=False)

    pedidoDistrDestino = Column(ForeignKey("distritos.distr_id"), name="distr_id", type_=types.Integer, nullable=False)

    cliente = Column(ForeignKey("clientes.cliente_id"), name="cliente_id", type_=types.Integer, nullable=False)
    


