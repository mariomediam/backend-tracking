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

class PlantillaRutasModel(base_de_datos.Model):
    __tablename__ = "plantillas_rutas"

    plantRutaId = Column(name="plant_ruta_id", type_=types.Integer, primary_key=True, nullable=False, autoincrement=True)

    distrDestino = Column(ForeignKey("distritos.distr_id"), name="distr_dest_id", type_=types.Integer, nullable=False)

    plantPasoNro = Column(name="paso_nro", type_=types.Integer, nullable=False)

    plantPasoTipo = Column(name="paso_tipo", type_=types.Enum(EnumTipoPaso))

    plantDescip = Column(name="paso_descrip", type_=types.String(100), nullable=False)

    plantTiempoEst = Column(name="tiempo_estimado", type_=types.Integer, nullable=False)




