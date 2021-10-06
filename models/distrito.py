from sqlalchemy.sql.sqltypes import String
from config.conexion_bd import base_de_datos
from sqlalchemy import Column, orm, types

class DistritoModel(base_de_datos.Model):
    __tablename__="distritos"

    distritoId = Column(name="distr_id", type_=types.Integer, primary_key=True, autoincrement=True, nullable=False)

    dptoNombre = Column(name="dpto_nombre", type_=String(50), nullable=False)

    provNombre = Column(name="prov_nombre", type_=String(50), nullable=False)

    distr_nombre = Column(name="distr_nombre", type_=types.String(50), nullable=False)

    
