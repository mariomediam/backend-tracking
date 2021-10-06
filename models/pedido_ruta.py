from sqlalchemy.sql.schema import ForeignKey
from config.conexion_bd import base_de_datos
from sqlalchemy import Column, types
from enum import Enum

class EnumTipoPaso(Enum):
    PAGADO = "Pagado"
    ENVIADO = "Enviado"
    EN_CAMINO = "En camino"
    EN_REPARTO = "En reparto"
    ENTREGADO = "Entregado"

class PedidoRutaModel(base_de_datos.Model):
    __tablename__ = "pedidos_rutas"

    pedRutaId = Column(name="ped_ruta_id", type_=types.Integer, primary_key=True, autoincrement=True, nullable=False)

    pedido = Column(ForeignKey("pedidos.pedido_id"), name = "pedido_id", type_=types.Integer, nullable=False)

    pedRutPasoNro = Column(name="paso_nro", type_=types.Integer, nullable=False)

    pedRutPasoTipo = Column(name="paso_tipo", type_=types.Enum(EnumTipoPaso))

    pedRutTiempoEst = Column(name="tiempo_estimado", type_=types.Integer, nullable=False)

    pedRutFechaEst = Column(name="fecha_estimada", type_=types.Date, nullable=False)

    pedRutRecibido = Column(name="recibido", type_=types.Boolean, default=False, nullable=False)

    pedRutFechaReal = Column(name="fecha_real", type_=types.Date, nullable=True)

    pedRutaComent = Column(name="comentario", type_=types.Text, nullable=True)

