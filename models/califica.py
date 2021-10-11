#from sqlalchemy.sql.expression import null
from sqlalchemy.sql.schema import ForeignKey
from config.conexion_bd import base_de_datos
from sqlalchemy import Column, types

class CalificaModel(base_de_datos.Model):
    __tablename__ = "calificaciones"

    calificaId = Column(name="califica_id", type_=types.Integer, primary_key=True, autoincrement=True, nullable=False)

    calificaToken = Column(name="token", type_=types.String(20), unique=True, nullable=False)

    pedido = Column(ForeignKey("pedidos.pedido_id"), name = "pedido_id", type_=types.Integer, nullable=False)

    calificaNota = Column(name="nota", type_=types.Integer, nullable=True)

    calificaComent = Column(name="comentario", type_=types.Text, nullable=True)



